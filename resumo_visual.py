import json,pathlib,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from matplotlib.colors import TwoSlopeNorm
import numpy as np
P=pathlib.Path(__file__).parent;D=json.load(open(P/'resultado.json'));plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11});fig=plt.figure(figsize=(16,11),facecolor='#f2f6f3');gs=fig.add_gridspec(2,2,height_ratios=[1,1.35],hspace=.36,wspace=.6,left=.18,right=.96,top=.86,bottom=.07)
fig.text(.07,.95,'Marina Bragante · correlação dos votos por seção',fontsize=25,weight='bold',color='#163e32');fig.text(.07,.907,'SP · 1º turno de 2026 · 103.656 seções · 2.415 outras candidaturas',fontsize=13,color='#536e60')
for col,o in enumerate([6,7]):
 ax=fig.add_subplot(gs[0,col]);rs=[r for r in D['results'] if r['office']==o and r['eligible']][:7];yy=np.arange(len(rs));ax.barh(yy,[r['r_share'] for r in rs],color='#267a60' if o==6 else '#527a93',height=.66);ax.set_yticks(yy,[r['name'] for r in rs]);ax.invert_yaxis();ax.set_xlim(0,1);ax.set_title('Deputado federal' if o==6 else 'Deputado estadual',loc='left',fontweight='bold',pad=15)
 for y,r in zip(yy,rs):ax.text(r['r_share']+.015,y,f"{r['r_share']:.3f}".replace('.',','),va='center',fontsize=11)
 ax.spines[['right','top','left']].set_visible(False);ax.tick_params(axis='y',length=0);ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True);ax.set_xlabel('Pearson das proporções por seção');ax.set_facecolor('#f2f6f3')
ax=fig.add_subplot(gs[1,0]);ref=next(r for r in D['results'] if r['key']=='6:4044');cmap=matplotlib.colors.LinearSegmentedColormap.from_list('correlacao',['#be4e46','#f8f8ef','#1e805b']);norm=TwoSlopeNorm(vmin=-1,vcenter=0,vmax=1);geom=D['map'];count=0
for m in geom['municipalities']:
 tokens=re.findall(r'[MLZmlz]|-?\d+(?:\.\d+)?',m['path']);verts=[];cmds=[];i=0;cmd=None
 while i<len(tokens):
  if tokens[i] in 'MLZmlz':
   cmd=tokens[i].upper();i+=1
   if cmd=='Z':
    if verts:verts.append(verts[0]);cmds.append(MPath.CLOSEPOLY)
    continue
  if i+1>=len(tokens):break
  verts.append((float(tokens[i]),-float(tokens[i+1])));cmds.append(MPath.MOVETO if cmd=='M' else MPath.LINETO);cmd='L';i+=2
 v=D['local'].get(m['id'],{}).get('r',[None]*(ref['index']+1))[ref['index']];count+=v is not None;ax.add_patch(PathPatch(MPath(verts,cmds),facecolor='#dce2dd' if v is None else cmap(norm(v)),edgecolor='white',linewidth=.25))
ax.set_xlim(0,geom['width']);ax.set_ylim(-geom['height'],0);ax.set_aspect('equal');ax.axis('off');ax.set_title('Bragante × Helou · correlação local',loc='left',weight='bold');sm=plt.cm.ScalarMappable(norm=norm,cmap=cmap);fig.colorbar(sm,ax=ax,orientation='horizontal',shrink=.65,pad=.03,label='Pearson entre seções dentro de cada município')
ax=fig.add_subplot(gs[1,1]);ax.axis('off');ax.text(0,1,'O padrão persiste dentro das zonas?',fontsize=17,weight='bold',va='top',color='#163e32');tx=[('Helou · Pearson das proporções',ref['r_share']),('Helou · dentro das mesmas zonas',ref['r_within']),('Tabata · Pearson das proporções',next(r for r in D['results'] if r['key']=='6:4040')['r_share']),('Tabata · dentro das mesmas zonas',next(r for r in D['results'] if r['key']=='6:4040')['r_within'])]
for i,(label,value) in enumerate(tx):
 ax.text(0,.80-i*.13,label,fontsize=12,color='#486454');ax.text(.93,.80-i*.13,f'{value:.3f}'.replace('.',','),fontsize=17,weight='bold',ha='right',color='#19563e')
ax.text(0,.20,'Correlação territorial não identifica os mesmos eleitores.\nTambém não significa votação de tamanho semelhante.\nRanking inicial: ≥1.000 votos e ≥100 seções com votos.\nMapa: cinza indica base insuficiente nos filtros locais.',fontsize=11,color='#516b5b',va='top',linespacing=1.7)
fig.text(.07,.015,'Fonte: TSE · votação por seção de SP · geração 06/10/2026. Resultados exploratórios; não demonstram dobrada ou transferência de votos.',fontsize=10,color='#577461');fig.savefig(P/'mapa-correlacao-bragante.png',dpi=150,facecolor=fig.get_facecolor());print('visual generated')
