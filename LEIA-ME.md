# Correlação dos votos de Marina Bragante por seção — SP 2026

## Entregas

- `correlacao-bragante-SP-2026.html`: relatório interativo, autocontido e offline. Abra no navegador, sem servidor ou internet.
- `ranking-correlacoes.csv`: todas as 2.415 comparações, sem os filtros de votação mínima da interface.
- `mapa-correlacao-bragante.png`: resumo estático para compartilhar.
- Scripts, matriz esparsa e metadados para reproduzir o cálculo.

Nenhum site foi publicado. A coleta parcial da Urna viva foi substituída pelo arquivo oficial completo do TSE.

## Base

Fonte: https://dadosabertos.tse.jus.br/dataset/resultados-2026

Arquivo SP: https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_SP.zip

Recorte: UF SP, primeiro turno, eleição 6259, cargos 6 (deputado federal) e 7 (deputado estadual). Geração da fonte: 06/10/2026, 14:03:43. A data exata e o SHA-256 estão em `base.json` e no relatório.

103.656 seções distintas, indexadas por município TSE + zona + seção. Todas têm denominadores positivos para os dois cargos. A origem contém 17.043.634 linhas e 767.459.830 bytes compactados; somente cargos e turno selecionados compõem a matriz. Existem votos para 2.416 candidaturas: Bragante e 2.415 outras (1.066 federais e 1.349 estaduais). Candidaturas sem qualquer voto registrado não têm coeficiente de correlação e não aparecem como comparações numéricas.

Bragante: 78.957 votos; pelo menos um voto em 29.100 seções. O total fecha com o usado no relatório anterior. Fotos, nomes de urna e partidos não participam do cálculo. Os rótulos de candidatura usam o catálogo 2026 da Urna viva quando há correspondência exata de cargo+número; nos demais casos o nome vem do próprio arquivo e o partido fica marcado como não vinculado ao catálogo.

## Métricas

1. `r_raw`: Pearson dos votos absolutos nas mesmas seções.
2. `r_share`: Pearson das proporções. Dividimos os votos de cada candidatura pelo total nominal + legenda do respectivo cargo na seção; excluímos 95/brancos e 96/nulos. Outros códigos especiais 97–99 também são excluídos se existirem. O denominador é operacional, sem reclassificar a destinação jurídica dos votos.
3. `spearman`: Spearman das proporções, postos médios em empates.
4. `r_within`: Pearson dos resíduos após remover a média de cada variável por município×zona eleitoral.
5. `r_capital`: Pearson das proporções apenas no município de São Paulo, código TSE 71072.
6. `r_positive`: Pearson das proporções nas seções em que Bragante teve votos. É uma análise condicional, não substitui a estadual.
7. `countCoverageReference` e `countCoverageOther`: soma de min(votos_Bragante, votos_outro) dividida pelo total respectivo. Comparam contagens agregadas, não eleitores em comum.

O ranking abre com mínimo de 1.000 votos e presença em 100 seções para reduzir destaque a candidaturas pequenas. Esses critérios são de exploração, não de validade estatística. O CSV completo inclui as votações pequenas, e a interface permite remover os filtros. A referência não é comparada a ela mesma.

O mapa calcula Pearson das proporções entre as seções dentro de cada município ou zona da capital. Mostramos um coeficiente local somente com pelo menos 50 seções, Bragante com votos em 10 seções e a outra candidatura com pelo menos 50 votos em 10 seções; é necessário haver variância. Valores ausentes por insuficiência aparecem em cinza. Não os substituímos por zero.

O mapa municipal usa geometria IBGE/TSE do projeto Urna viva. A malha de zonas da capital é CEM/USP 2024; zonas sem correspondência geométrica não são desenhadas. Não há geolocalização fictícia de seções.

A dispersão usa todas as 103.656 seções, agregadas em células de densidade 80×80 para cada candidatura. Não há amostragem ou descarte de pontos; a soma das células é verificada. Os eixos usam log(1 + proporção × 10.000), com rótulos em percentual.

## Reprodução sem baixar novamente o CSV de 5 GB

Requisitos: Python 3.11+; `numpy`, `scipy`. A renderização do resumo PNG também exige `matplotlib`.

```bash
python3 calcular.py
python3 gerar_html.py
python3 verificar.py
python3 resumo_visual.py
```

A matriz `votos.npz`, `secoes.npy`, `codigos.npy`, `base.json`, `catalogo.json` e as duas geometrias estão incluídas no pacote. Isso permite reproduzir as medidas sem o ZIP original do TSE. `calcular.py` também gera a matriz de proporções e o JSON intermediário, que podem ser removidos após gerar o HTML.

Para refazer desde a fonte oficial, instale também `pandas`:

```bash
python3 baixar.py
python3 preparar.py
python3 calcular.py
python3 gerar_html.py
```

O download exige cerca de 768 MB; o CSV é lido diretamente do ZIP em lotes, sem extrair 5 GB no disco. `base.json` registra o hash do arquivo efetivamente utilizado. Use a mesma fonte se quiser reproduzir exatamente esta versão; retotalizações futuras podem mudar o arquivo.

## Verificação e limitações

Verificamos unicidade das seções, limites dos coeficientes, soma dos votos e conservação de pontos na dispersão. Pearson absoluto, Pearson de proporções, Spearman e o ajuste por zona para Helou e Tabata foram conferidos com chamadas independentes de scipy.stats. A zona 251/Pinheiros tem 327 seções no arquivo completo e 7.283 votos para Bragante.

O código do HTML foi executado em ambiente DOM simulado: ranking inicial, filtro por cargo, seleção de candidato, troca de geografia, Pinheiros e chamadas de desenho de densidade passaram. A tentativa de teste real com Playwright ficou bloqueada pela ausência do executável Chromium. Nenhum navegador foi instalado. A imagem estática foi renderizada e inspecionada; a conferência do HTML em navegador permanece pendente.

Esta é uma exploração territorial descritiva, sem significância ajustada por milhares de comparações ou validação em outra eleição. Há efeito de zeros, concentração geográfica, composição da votação e valores extremos. Não se identifica voto individual, dobrada, transferência de voto, campanha conjunta ou causalidade. Duas candidaturas ao mesmo cargo não podem receber o voto da mesma pessoa para esse cargo no mesmo turno.
