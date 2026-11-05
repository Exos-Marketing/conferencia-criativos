# conferencia-criativos

Skill do Claude Code que faz a **conferência de criativos × copy** numa task do
ClickUp da Exos: criativos de imagem, banners, cards e vídeos. Ela entrega um
parecer por ADS (texto × copy, posicionamento em print com a interface do
Instagram por cima, conteúdo e pontos de decisão) e o rascunho do comentário
para quem produziu, só com o que precisa de ajuste.

```
task de criativos  →  anexos + copy  →  OCR + réguas  →  prints  →  parecer + rascunho  →  OK do Cleber  →  envio
   (ClickUp)          (baixar.py)      (ocr/regua)     (prints.py)                                       (postar.py)
```

## Por que ela existe

A revisão de criativo travava em duas coisas: o ajuste vinha em rodadas (cada
olhada achava um ponto novo) e "margem de 45 px" solto no texto não diz ao
designer o que a interface cobre. A skill revisa tudo de uma vez, por ADS,
e mostra o posicionamento em print.

## Instalação

```bash
git clone https://github.com/Exos-Marketing/conferencia-criativos.git \
  ~/.claude/skills/conferencia-criativos
```

Requisitos:

- **macOS**, porque o OCR é o Vision da Apple e os prints usam a Helvetica do sistema.
- Um Python em `~/.exos-whisper` com `pyobjc-framework-Vision`, `Pillow` e `numpy`:

  ```bash
  python3 -m venv ~/.exos-whisper
  ~/.exos-whisper/bin/pip install pyobjc-framework-Vision pillow numpy
  ```

- `ffmpeg` e `ffprobe` no PATH, só para conferir vídeo (`vid_diff.py`).
- O **seu** token da API do ClickUp no Keychain, no serviço `clickup-exos-api`:

  ```bash
  security add-generic-password -s clickup-exos-api -a "$USER" -w <seu-token>
  ```

  Também dá para passar o token na variável `CLICKUP_TOKEN`. Os scripts nunca imprimem o token.

**Nenhuma credencial mora neste repo.**

## Uso

No Claude Code, peça "confere os criativos da task <link>". A skill dispara
sozinha. Os scripts rodam nesta ordem:

```bash
SK=~/.claude/skills/conferencia-criativos/scripts; PY="$HOME/.exos-whisper/bin/python -I"
$PY $SK/baixar.py <task_id|url> <pasta nova>     # anexos, copy linkada e resumo da task
$PY $SK/ocr.py <pasta>/ocr.json <pasta>/dl/*.png  # texto + caixas em px
$PY $SK/regua.py <pasta>/ocr.json                 # réguas por formato e borda de 1 px
$PY $SK/prints.py <pasta>/prints.json             # prints Stories × Reels e feed
$PY $SK/postar.py <pasta>/envio.json              # prévia exata do envio (não escreve)
$PY $SK/postar.py <pasta>/envio.json --apply      # só depois do "pode enviar"
```

## A regra que não se negocia

**Nada vai para a task antes de o Cleber ver o comentário e autorizar**: nem
anexo, nem comentário, nem status, nem responsável. Sem `--apply`, o
`postar.py` só mostra a prévia. A autorização vale para o texto mostrado: se o
texto mudar, ele é mostrado de novo.

## O que tem aqui

| arquivo | o que faz |
|---|---|
| `SKILL.md` | o fluxo, as 5 regras e o formato do comentário |
| `REFERENCE.md` | as réguas por formato, os falsos alarmes do OCR, as decisões já tomadas, a receita de vídeo e o envio pela REST |
| `EXAMPLES.md` | um caso real completo: parecer, `comentario.md`, `envio.json` e `prints.json` |
| `scripts/baixar.py` | lê a task, baixa os anexos e a copy linkada |
| `scripts/ocr.py` | OCR do Vision com caixas em px |
| `scripts/regua.py` | passa as réguas e procura linha de 1 px na borda |
| `scripts/prints.py` | desenha a interface do Instagram por cima da peça |
| `scripts/postar.py` | prévia e envio: anexa os prints, comenta com @menção e atribuído, muda status e responsável e relê tudo |
| `scripts/vid_diff.py` | compara o vídeo reaproveitado com o editado aprovado: quadro a quadro, áudio e loudness |
| `scripts/clickup_api.py` | REST do ClickUp com o token do Keychain |

---

Interno · Exos Marketing Digital e Internacionalização Ltda.
