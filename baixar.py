import urllib.request,pathlib,time,json
p=pathlib.Path(__file__).parent;u='https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_SP.zip';t=time.time();path=p/'votacao_secao_2026_SP.zip'
try:
 with urllib.request.urlopen(u,timeout=45) as r,open(path,'wb') as f:
  print('status',r.status,'bytes',r.headers.get('Content-Length'),flush=True);n=0
  while True:
   b=r.read(1024*1024)
   if not b:break
   f.write(b);n+=len(b)
   if n%(50*1024*1024)==0:print('MB',n//1024//1024,flush=True)
 print('downloaded',n,'seconds',time.time()-t,flush=True)
except Exception as e:print(type(e).__name__,str(e),flush=True)
