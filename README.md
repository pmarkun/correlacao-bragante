# Correlação territorial · Marina Bragante

Relatório interativo com ranking, filtros, mapa e dispersão a partir da base recebida no pacote `correlacao-bragante-reproduzivel.zip`.

**Site:** https://pmarkun.github.io/correlacao-bragante/

## Usar

Selecione uma candidatura e escolha entre municípios de SP e zonas da capital. O botão **Exportar mapa em PNG** salva o recorte selecionado, com legenda, identificação da candidatura, fonte declarada e limites da análise. A imagem tem 1.800 pixels de largura e fundo branco.

Para executar localmente, use `sh iniciar.sh` e abra http://127.0.0.1:8765. Também é possível abrir `index.html` diretamente, mantendo `exportar-mapa.js` na mesma pasta.

## Dados e reprodução

Veja [LEIA-ME.md](LEIA-ME.md) para a metodologia e os scripts originais. As declarações de origem e os valores são os do pacote recebido; a adaptação para web não refez nem auditou os cálculos. Não há atualização automática. Correlação territorial não identifica eleitores em comum nem comprova causalidade.

`template-correlacao.html` é o modelo, `gerar_html.py` gera `index.html` após o cálculo e `exportar-mapa.js` implementa a exportação. A base incorporada ao HTML permite explorar o site sem chamadas a serviços de dados.

## Publicação

GitHub Pages serve a raiz da branch `feat/exportacao-mapa-pages`. O arquivo `.nojekyll` desativa o processamento Jekyll. O caminho `healthz` responde com um estado estático de disponibilidade dos arquivos; não valida os cálculos.

Validação: Chrome em 1440×900 e 390×844; ranking, seleção, geografia e geração de PNG para ambos os mapas. Firefox, Safari e aparelhos físicos não foram validados.
