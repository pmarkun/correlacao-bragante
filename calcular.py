"""Correlação eleitoral agregada por seção. Nenhuma inferência individual.
Python 3 + numpy, scipy. Use preparar.py antes de executar.
"""
import json,pathlib,datetime,csv,time
import numpy as np
from scipy import sparse,stats
P=pathlib.Path(__file__).parent;t=time.time();base=json.load(open(P/'base.json'));X=sparse.load_npz(P/'votos.npz');sec=np.load(P/'secoes.npy');codes=np.load(P/'codigos.npy');off=codes//100000;number=codes%100000
print('specials',[(int(c),base['names'][str(c)]) for c in codes if c%100000<100],flush=True)
valid=(~np.isin(number,[95,96,97,98,99]));den={str(o):np.asarray(X[:,(off==o)&valid].sum(axis=1)).ravel() for o in [6,7]}
use=(den['6']>0)&(den['7']>0);X=X[use];sec=sec[use];den={k:v[use] for k,v in den.items()};cand=number>99;C=codes[cand];V=X[:,cand].tocsc();n=len(sec)
catp=P/'catalogo.json';cat=json.load(open(catp)) if catp.exists() else []
lookup={int(c['office'])*100000+int(c['number']):c for c in cat}
refcode=740444;idx=int(np.flatnonzero(C==refcode)[0]);x=V[:,idx].toarray().ravel();xp=x/den['7'];nr=np.asarray(V.getnnz(axis=0)).ravel();totals=np.asarray(V.sum(axis=0)).ravel()
# Divisão pelo total registrado do cargo em cada seção, incluindo legenda.
Y=V.tocoo(copy=True);Y.data/=np.where(C[Y.col]//100000==6,den['6'][Y.row],den['7'][Y.row]);Y=Y.tocsc()
# IMPORTANT: V e Y não podem compartilhar arrays; tocoo cria cópia.
def pearson_all(M,xx):
 sx=xx.sum();vx=np.dot(xx,xx)-sx*sx/len(xx);sy=np.asarray(M.sum(axis=0)).ravel();vy=np.asarray(M.multiply(M).sum(axis=0)).ravel()-sy*sy/len(xx);cov=np.asarray(xx@M).ravel()-sx*sy/len(xx);return np.divide(cov,np.sqrt(np.maximum(vx*vy,0)),out=np.full_like(cov,np.nan),where=vy>1e-18)
r_raw=pearson_all(V,x);r_share=pearson_all(Y,xp)
capital=(sec//100000000==71072);r_capital=pearson_all(Y[capital],xp[capital]);positive=x>0;r_positive=pearson_all(Y[positive],xp[positive])
# Descontar médias por município+zona: correlação dentro das mesmas zonas.
group=sec//10000;ug,g=np.unique(group,return_inverse=True);ng=np.bincount(g);G=sparse.csr_matrix((np.ones(n),(g,np.arange(n))),shape=(len(ug),n));GY=(G@Y).tocsr();gx=np.asarray(G@xp).ravel();sy=np.asarray(Y.sum(axis=0)).ravel();s2y=np.asarray(Y.multiply(Y).sum(axis=0)).ravel();vy=s2y-np.asarray(GY.multiply(GY).multiply((1/ng)[:,None]).sum(axis=0)).ravel();vx=np.dot(xp,xp)-np.sum(gx*gx/ng);cov=np.asarray(xp@Y).ravel()-np.asarray((gx/ng)@GY).ravel();r_within=np.divide(cov,np.sqrt(np.maximum(vx*vy,0)),out=np.full_like(cov,np.nan),where=vy>1e-18)
rankx=stats.rankdata(xp);rankx-=rankx.mean();ranknorm=np.linalg.norm(rankx);spearman=[]
for j in range(len(C)):
 yy=Y[:,j].toarray().ravel();ry=stats.rankdata(yy);ry-=ry.mean();norm=np.linalg.norm(ry);spearman.append(float(np.dot(rankx,ry)/(ranknorm*norm)) if norm else None)
 if j%400==0:print('rank',j,'seg',round(time.time()-t),flush=True)
# Mapas municipais: correlações calculadas ENTRE seções do município, sem misturar municípios.
mu=sec//100000000;mus=np.unique(mu);local={};mapped=0
Yr=Y.tocsr();Vr=V.tocsr()
localcapital={}
groups=[('municipal',str(m),np.flatnonzero(mu==m)) for m in mus]+[('capital',str(int(z)%10000).zfill(4),np.flatnonzero(group==z)) for z in ug if z//10000==71072]
for scope,key,ix in groups:
 xx=xp[ix];M=Yr[ix,:];nn=len(ix);support=int(np.count_nonzero(x[ix]));votes_ref=int(x[ix].sum());sums=np.asarray(Vr[ix,:].sum(axis=0)).ravel();nonzero=np.asarray(M.getnnz(axis=0)).ravel()
 rr=pearson_all(M,xx) if nn>=3 and np.std(xx)>0 else np.full(len(C),np.nan)
 eligible=(nn>=50)&(support>=10)&(sums>=50)&(nonzero>=10)&np.isfinite(rr);eligible[idx]=False
 ranks=np.flatnonzero(eligible);ranks=ranks[np.argsort(rr[ranks])[::-1]][:5]
 record={'n':nn,'referenceVotes':votes_ref,'referencePositiveSections':support,'top':[{'index':int(j),'r':round(float(rr[j]),6),'votes':int(sums[j])} for j in ranks],'r':[round(float(rr[j]),6) if eligible[j] else None for j in range(len(C))]}
 if scope=='municipal':local[key]=record;mapped+=bool(len(ranks))
 else:localcapital[key]=record

results=[]
for j,c in enumerate(C):
 if c==refcode:continue
 cc=lookup.get(int(c),{});ys=V[:,j].toarray().ravel();both=int(np.count_nonzero((x>0)&(ys>0)));matched=float(np.minimum(x,ys).sum());record={'index':j,'key':str(c//100000)+':'+str(c%100000),'name':cc.get('name',base['names'][str(c)]),'party':cc.get('party','Não vinculado ao catálogo'),'office':int(c//100000),'number':str(c%100000),'votes':int(totals[j]),'positiveSections':int(nr[j]),'bothPositive':both,'r_capital':float(r_capital[j]) if np.isfinite(r_capital[j]) else None,'r_positive':float(r_positive[j]) if np.isfinite(r_positive[j]) else None,'r_raw':float(r_raw[j]) if np.isfinite(r_raw[j]) else None,'r_share':float(r_share[j]) if np.isfinite(r_share[j]) else None,'r_within':float(r_within[j]) if np.isfinite(r_within[j]) else None,'spearman':spearman[j],'countCoverageReference':matched/float(x.sum()),'countCoverageOther':matched/float(ys.sum()) if ys.sum() else None,'eligible':bool(totals[j]>=1000 and nr[j]>=100)};results.append(record)
results.sort(key=lambda r:-(r['r_share'] if r['r_share'] is not None else -2))
# Empacota valores por seção de TODOS os candidatos em representação esparsa.
sparse.save_npz(P/'proporcoes.npz',Y);np.save(P/'secoes_analise.npy',sec);np.save(P/'candidatos_analise.npy',C)
# Dispersão de densidade: todas as seções entram; células agregam contagens.
scatter={};xlog=np.log1p(xp*10000);xmax=float(xlog.max());xb=np.minimum(79,(xlog/xmax*80).astype(int))
for j in range(len(C)):
 yy=Y[:,j].toarray().ravel();yl=np.log1p(yy*10000);ymax=float(yl.max());yb=np.minimum(79,(yl/ymax*80).astype(int)) if ymax else np.zeros(n,dtype=int);hist=np.bincount(xb*80+yb,minlength=6400);bins=np.flatnonzero(hist)
 scatter[str(j)]={'xmax':round(xmax,6),'ymax':round(ymax,6),'cells':[[int(k//80),int(k%80),int(hist[k])] for k in bins]}
geom=json.load(open(P/'map.json'))
out={'reference':{'name':'Marina Bragante','number':'40444','office':7,'votes':int(x.sum()),'positiveSections':int(np.count_nonzero(x))},'n':n,'excludedSectionsNoDenominator':int((~use).sum()),'municipalityNames':base['municipalities'],'results':results,'local':local,'localCapital':localcapital,'map':geom,'capitalMap':json.load(open(P/'capital-zones.json')),'scatter':scatter,'source':{k:base[k] for k in ['source','snapshot_generations','source_bytes','sha256','source_rows','sections']},'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mappedMunicipalities':mapped}
(P/'resultado.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'),allow_nan=False))
with open(P/'ranking-correlacoes.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
print('RESULT',n,len(results),'target',out['reference'],'mapped',mapped,flush=True)
for o in [7,6]:print('TOP',o,[(r['name'],round(r['r_share'],4),round(r['r_within'],4),round(r['spearman'],4)) for r in results if r['office']==o and r['eligible']][:10],flush=True)
print('seconds',time.time()-t,flush=True)
