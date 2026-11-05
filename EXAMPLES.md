# Exemplo — Criativos de Imagem de Antecipação [DM][BF][POS][NOV][26] (20/10/26)

Task `17tqamewuwr`, Patrick (designer). Nove anexos: ADS 01 e ADS 01B em 1350 e 1920, banner dos vídeos em 1920 e
1440, banners Desktop, Mobile e YouTube. A copy está no Doc `8ckf9qa-750593`, página `8ckf9qa-748213`. O precedente
é a mesma task da ET (`17tqamemrq7`) e da LL (`86akezykm`), as duas aprovadas.

## Parecer (um bloco por ADS, todos os pontos)

```
### ADS 01 · 1080x1350 e 1080x1920
- Texto: headline e rodapé "EXCLUSIVO PARA PROFISSIONAIS FORMADAS(OS)" iguais à copy.
- Posicionamento: no 1350 a headline fica a 45–48 px (régua 45; só a ponta da serifa do "P" chega a 42).
  No 1920/Stories, y 387–1510, ok. No 1920/Reels o rodapé encosta no nome do perfil (print).
- Conteúdo: foto séria olhando para a câmera e composição da referência, ok.
- Decisões: fundo vinho × "preto" da copy; sem ♾️; só "11/11", sem a hora (recomendação para cada uma).
```

Depois dos blocos vêm as decisões numeradas, cada uma com a recomendação, e o rascunho do comentário.

## comentario.md (o que foi postado, comentário `1400480000365044`)

```
@Patrick Guilherme ajustes nos criativos de antecipação. Urgente: o ADS 01 vai ao feed e ao tráfego amanhã (qua 21/10).
Os 3 prints de posicionamento estão anexados na task. Neles, a faixa hachurada do Reels é a área que o Meta recomenda deixar livre; o pedido aqui é tirar o texto de baixo do nome do perfil, da legenda e dos ícones.

## ADS 01 [Antecipação] · 1080x1350 e 1080x1920
- Nos dois formatos: incluir o símbolo ♾️, discreto, junto do "ANTES DE 11/11". O planejamento da Black Infinita pede o ♾️ em todas as artes.
- Só no 1080x1920: subir o rodapé "EXCLUSIVO PARA PROFISSIONAIS FORMADAS(OS)" uns 60 px, até terminar acima de y≈1450. No Reels, ele encosta no nome do perfil. Print: [[Conferência - ADS 01 1080x1920 - posicionamento]]

## ADS 01B [Antecipação Teste AB] · 1080x1350 e 1080x1920
- Nos dois formatos: no rodapé, trocar "Exclusivo para profissionais formadas(os)" por "EXCLUSIVO PARA PROFISSIONAIS FORMADAS(OS)", em caixa alta como na copy.
- Só no 1080x1920: subir o rodapé (Revelação · Cadastros · Exclusivo), e os cards junto, até o rodapé terminar acima de y≈1450. No Reels, a linha "Exclusivo" fica atrás do nome do perfil e "Cadastros" encosta nele.
- Só no 1080x1920: manter o texto dos cards à esquerda de x≈960. Hoje o card da direita vai até x 1030 e fica atrás dos ícones de curtir e comentar. Print: [[Conferência - ADS 01B 1080x1920 - posicionamento]]

## Banner Criativos em Vídeo [Antecipação] · 1080x1920 e 1080x1440
- Nos dois formatos: em "NA TURMA DE FUNDADORES", abrir o espaço entre "NA" e "TURMA". Hoje são 5 a 7 px; entre as outras palavras são 11 a 13 px.
- Só no 1080x1920: subir a caixa "11/11 · 20h · AO VIVO" e a linha "EXCLUSIVO" até terminarem acima de y≈1450. No Reels, a linha EXCLUSIVO fica atrás do nome do perfil e a caixa da data encosta nele. Print: [[Conferência - Banner Criativos em Vídeo 1080x1920 - posicionamento]]
```

## envio.json

```json
{
  "task_id": "17tqamewuwr",
  "responsavel": {"id": 54941517, "nome": "Patrick Guilherme"},
  "tirar_responsaveis": [54927970],
  "status": "em alteração & ajuste",
  "comentario": "comentario.md",
  "prints": [
    "prints/Conferência - ADS 01 1080x1920 - posicionamento.png",
    "prints/Conferência - ADS 01B 1080x1920 - posicionamento.png",
    "prints/Conferência - Banner Criativos em Vídeo 1080x1920 - posicionamento.png"
  ]
}
```

IDs da equipe: Patrick `54941517` (Designer), Fernando `60428351` (Editor de Vídeos), Maurício `87901690`
(Copywriter), Gabriel `55123416`, Pedro `290496564`, Cleber `54927970`. Confira na task: o `baixar.py` lista os campos de função.

## prints.json (uma peça; as caixas estão em px do arquivo original)

```json
{
  "saida": "prints",
  "perfil": "dra.danielamoleiro",
  "pecas": [
    {
      "arquivo": "dl/ADS 01B [1080x1920] [Antecipação Teste AB] [DM][BF][POS][NOV][26].png",
      "nome": "Conferência - ADS 01B 1080x1920 - posicionamento.png",
      "titulo": "ADS 01B [1080x1920] [Antecipação Teste AB] [DM][BF][POS][NOV][26]",
      "stories": {"selo": ["OK", "verde"], "itens": [
        [1, [62, 252, 563, 500], "amarelo", "Caixinha da pergunta: começa em y=252, 2 px abaixo da faixa do perfil (250). Passa, no limite."],
        [2, [59, 1094, 1030, 1308], "verde", "Cards (y 1094 a 1308): livres."],
        [3, [166, 1363, 913, 1557], "verde", "Rodapé: termina em y=1557, 23 px acima da faixa do botão (1580). Passa."]]},
      "reels": {"selo": ["RODAPÉ COBERTO", "vermelho"], "itens": [
        [1, [62, 252, 563, 500], "amarelo", "Caixinha: os 17 px de cima entram na faixa de 14% (269 px); ali fica só o título \"Reels\"."],
        [2, [59, 1094, 1030, 1308], "vermelho", "Cards: a base entra na faixa de 35% e a ponta do card da direita fica atrás dos ícones de curtir e comentar."],
        [3, [166, 1363, 913, 1557], "vermelho", "Rodapé: a linha Exclusivo fica atrás do nome do perfil e Cadastros encosta nele."]]}
    }
  ]
}
```

Peça de 1350 usa `"feed": {"selo": […], "itens": […]}` no lugar de `stories` e `reels`. O painel mostra as linhas
de 45 px e o corte da grade 3:4.

## Desfecho

O envio anexou os 3 prints, postou o comentário atribuído ao Patrick, passou a task para "em alteração & ajuste" e
deixou o Patrick como responsável. A conferência do envio passou inteira (saída 0). Na recorreção, confira de novo
contra os 7 itens do comentário.
