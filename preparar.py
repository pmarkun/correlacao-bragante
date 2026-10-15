import pathlib,json,time,zipfile,hashlib
import numpy as np,pandas as pd
from scipy import sparse
P=pathlib.Path(__file__).parent;t=time.time();parts=[];catalog={};municipalities={};rowsread=0;special={};raw=P/'votacao_secao_2026_SP.zip'
with zipfile.ZipFile(raw) as z:
 name=next(n for n in z.namelist() if n.lower().endswith('.csv'))
 with z.open(name) as f:
  reader=pd.read_csv(f,sep=';',encoding='latin1',usecols=['DT_GERACAO','HH_GERACAO','NR_TURNO','CD_ELEICAO','CD_MUNICIPIO','NM_MUNICIPIO','NR_ZONA','NR_SECAO','CD_CARGO','NR_VOTAVEL','NM_VOTAVEL','QT_VOTOS'],chunksize=400000)
  generations=set()
  for chunk in reader:
   rowsread+=len(chunk);df=chunk[(chunk.NR_TURNO==1)&chunk.CD_CARGO.isin([6,7])&(chunk.CD_ELEICAO==6259)]
   if df.empty:continue
   for a,b in df[['DT_GERACAO','HH_GERACAO']].drop_duplicates().itertuples(index=False,name=None):generations.add(a+' '+b)
   for code,nm in df[['CD_MUNICIPIO','NM_MUNICIPIO']].drop_duplicates().itertuples(index=False,name=None):municipalities[str(code)]=nm
   # A seção existe independentemente de ter voto nas candidaturas selecionadas.
   sid=df.CD_MUNICIPIO.to_numpy(np.int64)*100000000+df.NR_ZONA.to_numpy(np.int64)*10000+df.NR_SECAO.to_numpy(np.int64)
   office=df.CD_CARGO.to_numpy(np.int32);number=df.NR_VOTAVEL.to_numpy(np.int32);v=df.QT_VOTOS.to_numpy(np.float64)
   for o,n,nm in df[['CD_CARGO','NR_VOTAVEL','NM_VOTAVEL']].drop_duplicates().itertuples(index=False,name=None):catalog[int(o)*100000+int(n)]=str(nm)
   parts.append((sid,office*100000+number,v))
   print('linhas',rowsread,'seg',round(time.time()-t),flush=True)
ids=np.concatenate([p[0] for p in parts]);codes=np.concatenate([p[1] for p in parts]);votes=np.concatenate([p[2] for p in parts]);del parts
sections,ri=np.unique(ids,return_inverse=True);allcodes,ci=np.unique(codes,return_inverse=True);del ids,codes
X=sparse.coo_matrix((votes,(ri,ci)),shape=(len(sections),len(allcodes))).tocsr();del ri,ci,votes
sparse.save_npz(P/'votos.npz',X);np.save(P/'secoes.npy',sections);np.save(P/'codigos.npy',allcodes)
meta={'source':'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_SP.zip','snapshot_generations':sorted(generations),'sections':len(sections),'codes':len(allcodes),'matrix_nonzero':X.nnz,'source_rows':rowsread,'municipalities':municipalities,'names':{str(c):catalog[int(c)] for c in allcodes},'source_bytes':raw.stat().st_size,'sha256':hashlib.file_digest(raw.open('rb'),'sha256').hexdigest()}
(P/'base.json').write_text(json.dumps(meta,ensure_ascii=False));print('READY',X.shape,X.nnz,'seconds',time.time()-t,flush=True)
