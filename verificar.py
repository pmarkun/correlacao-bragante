import pathlib,json,numpy as np
from scipy import sparse,stats
P=pathlib.Path(__file__).parent;D=json.load(open(P/'resultado.json'));V=sparse.load_npz(P/'votos.npz').tocsc();codes=np.load(P/'codigos.npy');sec=np.load(P/'secoes.npy');off=codes//100000;num=codes%100000
ix=lambda c:int(np.flatnonzero(codes==c)[0]);den={o:np.asarray(V[:,(off==o)&(~np.isin(num,[95,96,97,98,99]))].sum(axis=1)).ravel() for o in [6,7]};x=V[:,ix(740444)].toarray().ravel();xs=x/den[7];groups=sec//10000;ug,g=np.unique(groups,return_inverse=True);counts=np.bincount(g);xr=xs-np.bincount(g,weights=xs)[g]/counts[g]
for key in ['6:4044','6:4040','7:40444']:
 o,n=map(int,key.split(':'));c=o*100000+n;y=V[:,ix(c)].toarray().ravel();ys=y/den[o]
 if c==740444:assert int(y.sum())==78957;continue
 r=next(r for r in D['results'] if r['key']==key);yr=ys-np.bincount(g,weights=ys)[g]/counts[g]
 assert abs(stats.pearsonr(x,y).statistic-r['r_raw'])<1e-10
 assert abs(stats.pearsonr(xs,ys).statistic-r['r_share'])<1e-10
 assert abs(stats.spearmanr(xs,ys).statistic-r['spearman'])<1e-10
 assert abs(stats.pearsonr(xr,yr).statistic-r['r_within'])<1e-10
 assert r['votes']==int(y.sum());print(key,'all coefficients verified')
assert len(sec)==103656 and len(np.unique(sec))==103656
assert len(D['results'])==len(set(r['key'] for r in D['results']))
for r in D['results']:
 for k in ['r_raw','r_share','r_within','spearman','r_capital','r_positive']:
  assert r[k] is None or -1.000000001<=r[k]<=1.000000001
for scat in D['scatter'].values():assert sum(c[2] for c in scat['cells'])==103656
z=D['localCapital']['0251'];assert z['n']==327 and z['referenceVotes']==7283
print('PASS unique sections, coefficients, scatter conservation, Pinheiros 327 sections. Reference:',D['reference'])
