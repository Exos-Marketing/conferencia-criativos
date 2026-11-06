---
name: conferencia-criativos
description: Confere criativos de imagem, banners e cards anexados numa task do ClickUp da Exos contra a copy e entrega ao Cleber o parecer por ADS (texto × copy, posicionamento em print com a interface do Instagram por cima — Stories × Reels e feed —, conteúdo e pontos de decisão) com o rascunho do comentário para quem produziu, só com o que precisa de ajuste. Só envia para a task (prints anexados, comentário atribuído, status "em alteração & ajuste", responsável) depois que o Cleber vê o comentário e autoriza. Use quando o usuário pedir "conferir os criativos", "conferência frente à copy", "revisar os ADS da task", "conferir os banners", "revisão dos criativos de imagem", ou mandar o link de uma task de criativos para revisão. Para vídeo o fluxo e o comentário são os mesmos; a varredura de fala e legenda está no REFERENCE.
---

# Conferência de criativos × copy

Scripts em `scripts/`, rodados com o Python do `~/.exos-whisper` (tem Vision, PIL e numpy). Réguas, falsos alarmes
e decisões já tomadas: [REFERENCE.md](REFERENCE.md). Caso real completo (parecer, comentário, spec dos prints,
envio): [EXAMPLES.md](EXAMPLES.md).

```bash
SK=~/.claude/skills/conferencia-criativos/scripts; PY="$HOME/.exos-whisper/bin/python -I"
C=<scratchpad>/conf_<sigla>_<peça>                       # pasta nova por conferência
$PY $SK/baixar.py <task_id|url> "$C"                     # anexos em $C/dl, copy em $C/copy_*.md, resumo da task
$PY $SK/ocr.py "$C/ocr.json" "$C"/dl/*.png               # texto + caixas em px
$PY $SK/regua.py "$C/ocr.json"                           # margens e faixas por formato, borda de 1 px
$PY $SK/prints.py "$C/prints.json"                       # prints de posicionamento (spec no EXAMPLES)
$PY $SK/postar.py "$C/envio.json"                        # prévia exata do envio (não escreve)
$PY $SK/postar.py "$C/envio.json" --apply                # só depois do "pode enviar"
```

## Regras

1. **Nada vai para a task antes de o Cleber ver o comentário e autorizar**: nem anexo, nem comentário, nem status,
   nem responsável. A autorização vale para o texto mostrado. Se o texto mudar, mostre de novo antes de enviar.
2. **Revisão de uma vez, por ADS.** Cada peça leva todos os seus pontos explicados (texto × copy, posicionamento,
   conteúdo e decisões). Nada fica para uma segunda rodada.
3. **Posicionamento sempre em print**, com a interface por cima e a explicação do que cobre o quê, em px.
   "Margem de 45 px" solto no texto não basta.
4. **Comentário só com o que precisa de ajuste.** Nada de "o texto bate", "aprovados" ou "a peça está ok". O que
   está certo e os pontos de decisão ficam no parecer.
5. **Precedente:** o que passou na task irmã aprovada (mesma peça, outro expert) não vira ajuste, vira decisão.
6. **Formato é o da copy.** Os tamanhos pedidos saem da configuração da copy, da peça ou do bloco. A descrição da
   task não serve de régua de formato. Se a copy não define formato, não há cobrança: vira pergunta no parecer.

## Fluxo

1. **Task.** `baixar.py` mostra status, responsável pela função (Designer, Editor de Vídeos), anexos e comentários.
   Leia a copy inteira: o cabeçalho (identidade, qualificador, regras "em toda peça"), cada ADS (texto,
   referência, configuração) e as observações. Se a copy cita o planejamento, leia a seção citada.
2. **Precedente.** Procure a task irmã aprovada (mesmo nome, outra sigla) e leia os anexos e o comentário de aprovação.
3. **Texto.** Rode `ocr.py` e compare linha a linha com a copy. Toda suspeita passa por zoom antes de virar ajuste.
4. **Posicionamento.** `regua.py` aponta o que está perto dos limites. Confirme no pixel, porque a caixa do OCR
   erra alguns px e não vê a placa atrás do texto. Peça de 1920 com algo no limite ou coberto ganha print
   Stories × Reels; peça de 1350 fora da margem ganha print de feed.
5. **Conteúdo.** Confira foto e cena (mãos, datas, palavras), identidade, ícones, borda de 1 px, nome de arquivo,
   formatos pedidos na copy × entregues (regra 6) e peças extras.
6. **Parecer.** Um bloco por ADS, na ordem da copy, com texto, posicionamento (com o print), conteúdo e decisões
   com recomendação. Depois vem o rascunho do comentário, já no formato abaixo.
7. **Autorização.** Espere o "pode enviar" e incorpore os cortes que ele pedir.
8. **Envio.** Escreva o `comentario.md` e o `envio.json` (modelos no EXAMPLES) e rode a prévia: ela tem de bater com
   o texto aprovado. Depois rode `--apply`: o script anexa os prints, posta o comentário com @menção e atribuído ao
   responsável, muda o status, troca o responsável e relê tudo. A saída 0 quer dizer que todas as conferências do
   envio passaram.
9. **Limpeza.** Apague os downloads logo depois do parecer e os prints depois de anexados. Registre o desfecho na
   memória do projeto.

## Comentário

```
@<Responsável> ajustes em <peças>. Urgente: <o que sobe quando>, se houver.
<uma linha sobre os prints, se houver>

## ADS 01 [Antecipação] · 1080x1350 e 1080x1920
- Nos dois formatos: <o que mudar>. <por quê, curto>.
- Só no 1080x1920: <o que mudar>. <o que atrapalha>. Print: [[Conferência - ADS 01 1080x1920 - posicionamento]]
```

O título do bloco é o nome da peça como está no arquivo. Ajuste que vale para várias peças se repete em cada bloco.
A ordem é a da copy; depois vêm as peças que faltam e, por último, o que não é ADS. O responsável é quem produziu
(campo Designer ou Editor de Vídeos, ou quem postou "anexados para revisão").

## Erros comuns

| Saída | O que fazer |
|---|---|
| `já existe e não está vazia` | uma pasta nova por conferência |
| `a 1ª linha do comentário tem de começar com '@…'` | o nome em `envio.json` tem de ser igual ao do ClickUp |
| `cita print que não está em 'prints'` | o texto entre `[[ ]]` tem de ser o nome do arquivo sem `.png` |
| `status '…' não existe na lista` | ler os status da lista; nas de processo é `em alteração & ajuste` |
| `comentário já existe` | o envio já foi feito; `--forcar` só se o Cleber pedir outro comentário |
| `FALHOU` na conferência do envio | reler a task antes de qualquer nova tentativa (escrita não repete sozinha) |
