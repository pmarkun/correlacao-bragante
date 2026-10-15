'use strict';

// Renderiza somente vetores e dados locais, sem imagens ou serviços externos.
async function exportMapPng() {
  const button = document.getElementById('exportMap');
  const status = document.getElementById('exportStatus');
  button.disabled = true;
  status.textContent = 'Preparando o PNG…';
  let svgUrl;
  try {
    // Captura a seleção antes de qualquer operação assíncrona.
    const svg = document.querySelector('#map svg').cloneNode(true);
    const candidate = chosen;
    const capital = document.getElementById('geo').value === 'capital';
    const geography = capital ? 'Capital · zonas eleitorais' : 'São Paulo · municípios';
    const box = svg.viewBox.baseVal;
    const width = 1800;
    const mapWidth = width - 120;
    const mapHeight = Math.round(mapWidth * box.height / box.width);
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('width', mapWidth);
    svg.setAttribute('height', mapHeight);
    svgUrl = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml;charset=utf-8' }));
    const picture = new Image();
    picture.src = svgUrl;
    await picture.decode();
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = mapHeight + 470;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#153535';
    ctx.font = 'bold 40px system-ui';
    ctx.fillText('Correlação territorial · Marina Bragante', 60, 70, width - 120);
    ctx.font = '30px system-ui';
    ctx.fillText(`Bragante × ${candidate.name}`, 60, 120, width - 120);
    ctx.fillStyle = '#506e63';
    ctx.font = '24px system-ui';
    ctx.fillText(`${geography} · ${candidate.office === 6 ? 'Federal' : 'Estadual'} · ${candidate.number} · ${candidate.party}`, 60, 164, width - 120);
    ctx.drawImage(picture, 60, 190, mapWidth, mapHeight);
    const y = mapHeight + 230;
    const gradient = ctx.createLinearGradient(100, 0, 440, 0);
    gradient.addColorStop(0, color(-1));
    gradient.addColorStop(0.5, color(0));
    gradient.addColorStop(1, color(1));
    ctx.fillStyle = gradient;
    ctx.fillRect(100, y, 340, 22);
    ctx.fillStyle = '#153535';
    ctx.font = '22px system-ui';
    ctx.fillText('−1', 60, y + 20);
    ctx.fillText('0', 263, y + 50);
    ctx.fillText('+1', 450, y + 20);
    ctx.fillStyle = color(null);
    ctx.fillRect(540, y, 28, 22);
    ctx.fillStyle = '#506e63';
    ctx.fillText('Base insuficiente', 582, y + 20);
    ctx.fillText('Pearson das proporções por seção dentro de cada área; cinza não significa zero.', 60, y + 90, width - 120);
    ctx.fillText('Filtros: ≥50 seções; Bragante em ≥10; outra candidatura ≥50 votos em ≥10; variância não nula.', 60, y + 125, width - 120);
    ctx.font = '20px system-ui';
    ctx.fillText(`Fonte declarada: TSE · SP 2026 · geração ${D.source.snapshot_generations.join(', ')}.`, 60, y + 160, width - 120);
    ctx.fillText('Análise descritiva: correlação territorial não identifica eleitores em comum nem causalidade.', 60, y + 192, width - 120);
    const png = await new Promise((resolve, reject) => canvas.toBlob(blob => blob ? resolve(blob) : reject(new Error('Falha ao gerar imagem')), 'image/png'));
    const url = URL.createObjectURL(png);
    const link = document.createElement('a');
    const slug = candidate.name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    link.href = url;
    link.download = `mapa-bragante-${slug}-${capital ? 'zonas-capital' : 'municipios-sp'}.png`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60000);
    status.textContent = 'PNG exportado com a candidatura e a geografia selecionadas.';
  } catch (error) {
    console.error('Falha ao exportar mapa:', error);
    status.textContent = 'Não foi possível gerar o PNG. Tente novamente.';
  } finally {
    if (svgUrl) URL.revokeObjectURL(svgUrl);
    button.disabled = false;
  }
}

document.getElementById('exportMap').addEventListener('click', exportMapPng);
