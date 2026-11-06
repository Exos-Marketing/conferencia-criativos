# Referência — réguas, falsos alarmes e decisões

## Posicionamento

| Formato | Régua | O que atrapalha |
|---|---|---|
| 1080x1350 (feed) | texto, selo e logo a **45 px** das bordas | a grade 3:4 do perfil corta ~34 px de cada lado; no feed, a imagem encosta na borda da tela |
| 1080x1920 anúncio, **Stories** (régua da casa) | nada em **y < 250** nem em **y > 1580** | em cima: barra de progresso, avatar, nome, "Patrocinado", "…" e X; embaixo: o botão "Saiba mais" (y≈1740–1812) |
| 1080x1920, **Reels** (guias de mercado) | 14% em cima (269 px), 35% embaixo (y > 1248), 6% nas laterais (65 px) | o nome do perfil e "Patrocinado" (y≈1490–1555), a legenda (1584, que cresce ao tocar em "mais"), o áudio (1628), o botão largo (1688–1760) e os ícones (x≈978–1042; y 1120, 1260, 1400 e 1540) |
| 1080x1920 só orgânico | 250 px em cima e embaixo (y > 1670) | escolha minha, sem confirmação do Cleber |
| Tela de live 1080x1920 | conteúdo em y≈300–1200 e x≈120–960 | o cabeçalho do Instagram, os comentários e o "entrou na live"; o celular corta ~100 px de cada lado; "EU QUERO" flutuante no canto superior esquerdo |
| YouTube 2560x1440 | área segura 1546x423 no centro (x 507–2053, y 508–931) | o corte de TV, desktop e celular; procurar emenda logo abaixo de y 931 (salto de luminância entre linhas) |

- **Reels (decisão do Cleber em 20/10/26, antecipação DM):** pediu os ajustes junto com os de texto, com a meta prática
  de tirar o texto de baixo da interface fechada: terminar acima de **y≈1450** e, na altura dos ícones, ficar à esquerda
  de **x≈960**. Cumprir os 35% inteiros obriga a remontar a peça. Ele não disse se o Reels virou régua fixa: leve-o
  no print e proponha o ajuste no rascunho. Só vale para 1920 que roda como anúncio: card só de stories fica fora, e o
  Orgânico acompanha o ADS só para o par continuar igual fora do CTA. Calcule também quanto dá para subir sem passar de
  y=250: se não couber só subindo, o pedido é subir e apertar, com os dois números.
- O banner de vídeo aprovado da ET (`17tqamemrq7`) tinha a data em y 1504–1576 e uma faixa "BLACK FRIDAY" dentro
  das duas zonas. O Reels nunca foi régua antes de 20/10.
- **Medir no pixel:** a caixa do OCR erra alguns px. Serifa itálica que passa 2–3 px da margem em 2 linhas de pixel (o
  "P" de "Profissional" a 42 px) não conta. Para a borda de placa ou caixa, procure a cor da placa por coluna e linha.
- **Banner de vídeo:** os formatos são os da copy. Se o vídeo sai em 1080x1440, o banner também tem de vir em 1440.
  Sem ele, o editor recorta o 1920 e o banner sai cortado.
- **Selo e assinatura em teste A/B:** o diff A × B tem de cair só no selo. Assinatura maior ou recentralizada na B é desvio.

## Texto × copy

- **Regras do cabeçalho** ("qualificador em toda peça", "data e hora em toda peça", "♾️ nas artes"): se o
  precedente passou sem a regra, ela vira ponto de decisão. Na DM (20/10/26) o Cleber pediu o ♾️ no ADS 01 e o
  qualificador em caixa alta no 01B. O ADS 01 só com a data e os banners da área de alunos sem qualificador ficaram como estavam.
- **Linha de data reaproveitada:** o designer repete a barra do 1º card nos cards em que a copy muda a linha.
- **CTA:** conte quantas vezes o CTA aparece no OCR de cada arquivo (já apareceu "Saiba Mais" duplicado). No par
  Pago × Orgânico, cruze o CTA lido com o nome de cada arquivo, formato por formato, porque já vieram nomes trocados.
- **Pago × Orgânico:** diff de pixels (PIL/numpy, limiar 40). Se a diferença ficar só na faixa do CTA, está ok;
  "idênticas" indica CTA trocado; diferença espalhada indica peça regerada. Umas 500 px na faixa do selo e do logo, sem
  deslocamento, é reexportação (contagem DM, 02/11/26): não é desvio.
- **Formatos (regra do Cleber, 05/11/26):** os tamanhos pedidos saem da configuração da copy, da peça ou do bloco.
  A descrição da task traz uma lista genérica ("1350x1080, 1080x1920 e 1920x1080") e não serve de régua. Procure
  "Formatos" ou "NNNNxNNNN" na copy da peça, no bloco e no cabeçalho. Se nada definir formato, não cobre: pergunte
  no parecer. As decisões antigas "1440 no lugar do 1350" e "sem 1920x1080" (LL 07/10, ET 31/10) vinham da
  descrição e não valem mais.
- **Peça modelada de referência:** baixe a REF. O que é da marca de origem e sobrou na peça é erro; o que a referência
  também tem não é invenção do designer.

## Falsos alarmes do OCR (dar zoom antes de cobrar)

- O Vision sem correção de idioma perde acento em caixa alta ("CONSULTORIO", "AS 20H"), e aspa reta em itálico parece curva.
- Em fonte fina, ele lê "Dra. Daniela" como "Dia.Daniela" e já errou "SAÚDE", "Íntima" e "20H".
- Palavras grudadas podem ser kerning de verdade: "NATURMA" era um vão de 5–7 px entre NA e TURMA, contra 11–13 px
  entre as outras palavras. Meça o vão por coluna antes de descartar como erro do OCR.
- Ponto final colado no emoji ("Fundadores.🖤") às vezes some no OCR.
- Logo Black Friday Infinita: o OCR lê "FODA", "SDDA", "BLAGK" e "INFINITAC", e a caixa de título com brilho ("POUCO" a 14 px)
  erra a margem. "AOVIVO" no título grande tinha vão de 36 px contra 15–19 px entre letras. Meça antes de cobrar.

## Conteúdo

- **Foto da expert:** o Cleber mandou trocar foto "bem diferente" dela (captação DM, 27/10/26). Monte uma folha com as fotos da
  peça ao lado das já aprovadas na campanha e deixe o julgamento para ele, que conhece o rosto. Dê zoom nas mãos, no degradê
  (dedo pela metade) e em botão ou joia que caia sobre uma letra.
- **Traço de corpo na cena** (quadro, arco, relevo): decisão, não ajuste. Pese se a peça roda num dia só, sem folga para
  uma reprovação na Meta.
- **Cena com data:** confira se o mês e o dia da semana batem com o período da campanha.
- **Texto decorativo na cena** (bordado, lombada): palavra cortada na borda vai para o ajuste; o resto, para decisão.
- **Selo de sigla sensível:** passe o OCR no selo. Se a copy pede monograma ilegível por máquina e o OCR lê a sigla, é decisão.
- **Borda de 1 px:** compare a última coluna/linha com a vizinha; salto médio acima de 30 indica linha de export (`regua.py` faz isso).
- **Peça extra** que a copy não pede (ex.: banner de YouTube): a pergunta de onde vai ser usada vai no parecer, não
  no comentário. Ela só entra no comentário se precisar de ajuste.
- **PDF com página nova:** confira os links da página (`get_links()` no pymupdf) e faça o diff de palavras contra o
  original. O Canva cola palavras ao reimportar PDF.

## Vídeo

Mesmo parecer e mesmo comentário por ADS, com minutagem. A receita da varredura está na memória
`reference_varredura_texto_midia_drive`:
- fala com o `mlx_whisper` (large-v3-turbo) e segunda opinião com faster-whisper ou wav2vec2;
- tela com quadros a 4–10 fps, OCR do Vision e folhas de recortes da faixa da legenda;
- `blackdetect` e `silencedetect` para preto e silêncio;
- "mídia offline" aparece no probe como −180 dB;
- banner final procurado no OCR e conferido contra a versão 1440;
- antes de cobrar o editor, transcreva o bruto: o desvio de fala pode ter vindo da gravação.
- **Vídeo reaproveitado (só troca de card ou ano, sem regravação):** compare com o editado aprovado do ano anterior,
  não com a copy. `scripts/vid_diff.py <novo> <antigo> <saida.json>` compara quadro a quadro e o áudio. Mesma contagem de
  quadros, áudio com correlação ≈0,9998 e imagem igual fora das janelas do card provam que fala, legenda, trilha e cortes
  ficaram como estavam. Dentro das janelas, confira mais do que o ano: a caixa atrás da data, a escala do card no 1920 e a
  duração e a transição de saída, porque um corte seco cobre a primeira legenda depois do card. No KM BF COMBO (28/10/26) a
  caixa branca da data sumiu no banner e nos 12 vídeos.
- **Volume e fim do reaproveitado:** compare `lufs26` × `lufs25` do `vid_diff`. Se a diferença relativa mediana por janela
  bater com a de ganho puro (20·log10|1−10^(g/20)|), é o mesmo áudio exportado mais baixo: nos orgânicos do KM (28/10/26),
  5 de 6 saíram 2,6–7,7 dB abaixo de 2025. Vídeo mais curto que o de 2025 = card final encurtado; confira com `astats` nos
  últimos 1,5 s se a música para seco (em 2025 havia fade).
- **Card com zoom lento:** NCC contra a arte parada perde o card quando ele dá zoom. Meça entrada, saída e zoom com NCC em
  várias escalas (1,00–1,42, centrado) e confirme as transições em quadros a 10 fps.
- **Legenda do post também é reaproveitada:** nos orgânicos, o "Texto - Conteúdo N" (Google Doc na pasta do ano anterior)
  vai junto. Exporte com `--drive-export-formats txt` e procure a mesma regra da peça (ano, "first time", "unprecedented").
  É copy, então entra no parecer, não no comentário ao editor.
- **"Sem ano" pode ser arquivo deduplicado:** na varredura, o orgânico idêntico a um ADS aparece só com o nome do ADS. No KM, os
  Conteúdos 2 e 8 de antecipação eram o ADS 02 e o ADS 06 1920 (mesmo tamanho no Drive), com o card e o ano. Confira o tamanho
  ou o md5 antes de aceitar que um conteúdo não tem ano.
- **Cada card contra o mesmo card de 2025:** compare o do meio com o do meio e o final com o final, em cada formato. Meça três
  coisas: a entrada, o fim e o zoom no último quadro. No KM, o zoom de 2026 chegava a 5 px das bordas e levava a data à linha do
  perfil no Reels. No card do meio isso virou ajuste. No card final não, porque o de 2025 aprovado já terminava assim, e esse é o
  precedente. Diferença de 0,5 s no card final que não cobre fala nem legenda fica no parecer.

## Envio (ClickUp REST, token no Keychain `clickup-exos-api`)

- **Comentário:** `POST /api/v2/task/{id}/comment` com o array `comment` e `"assignee": uid` no corpo. Os blocos são
  `{"type":"tag","user":{"id":uid}}` (menção), `{"text":…, "attributes":{"bold":true}}` e
  `{"text":…, "attributes":{"link":url}}`. No `comment_text`, a menção aparece no fim; na tela ela aparece no começo.
- **Status:** o nome é exato e varia por lista. Nas listas de processo (Copywriting `901301657744`, Design
  `901301657750`) é `em alteração & ajuste`.
- **Responsável:** o Space Marketing aceita só um. O script tenta `add` + `rem` juntos e, se der erro, tira primeiro e
  põe depois. Convidado sem acesso dá ITEM_087: compartilhe a task com ele antes.
- **Anexo:** `POST /api/v2/task/{id}/attachment` (multipart, campo `attachment`). O nome do print fica "Conferência - <peça> <formato> - posicionamento.png".
- **Conferência sem ajuste:** não muda status nem responsável. A aprovação é um comentário do Cleber (ex.:
  "aprovado, agendar no orgânico conforme a copy").
