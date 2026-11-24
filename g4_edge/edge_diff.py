# Edge-case differential: frozen clean-room ref (Link copy, effc85ac) vs core ba2ea57 via libdr.so. Seed 20261124. Synthetic only, no DS1/DS2.
import sys, ctypes, json, collections, numpy as np
sys.dont_write_bytecode=True; sys.path.insert(0,'/workspace/link/dr_cleanroom_frozen_v1')
from ref import tier as ref_tier
L=ctypes.CDLL('/workspace/dr_job3/ds1/libdr.so'); NAMES=['None','T1','T2','T3']
def core(a):
    a=np.ascontiguousarray(a,dtype=np.int64); c=ctypes.c_int(); t=ctypes.c_int(); s=ctypes.c_float(); k=ctypes.c_float()
    L.ev(a.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),ctypes.c_ulong(len(a)),ctypes.byref(c),ctypes.byref(t),ctypes.byref(s),ctypes.byref(k))
    return NAMES[t.value]
rng=np.random.default_rng(20261124)
def gen(kind,n):
    if kind=='iid': return rng.integers(0,2048,n)
    if kind=='walk': return np.cumsum(rng.integers(-3,4,n))+1024
    if kind=='tie_heavy': return (np.cumsum(rng.normal(0,1,n))//4).astype(int)
    if kind=='sine_noise': return (512*np.sin(np.arange(n)/20)+rng.normal(0,8,n)).astype(int)
    if kind=='no_ties_monotone': return np.arange(n)*2+rng.integers(0,2,n)
NS=[64,256,513,514,1024,1025,4096]; KINDS=['iid','walk','tie_heavy','sine_noise','no_ties_monotone']
rows=[]; 
for n in NS:
    for k in KINDS:
        for r in range(40):
            a=gen(k,n); rt=ref_tier(list(map(int,a)))[0]; ct=core(a); rows.append((n,k,rt,ct))
tot=len(rows); agree=sum(r[2]==r[3] for r in rows)
byN={n:(sum(1 for r in rows if r[0]==n and r[2]==r[3]),sum(1 for r in rows if r[0]==n)) for n in NS}
byK={k:(sum(1 for r in rows if r[1]==k and r[2]==r[3]),sum(1 for r in rows if r[1]==k)) for k in KINDS}
conf=collections.Counter((r[3],r[2]) for r in rows)
out={'total':tot,'agree':agree,'by_N':byN,'by_kind':byK,'confusion_core_to_ref':{f'{a}->{b}':v for (a,b),v in sorted(conf.items())}}
json.dump(out,open('edge_results.json','w'),indent=1); print(json.dumps(out,indent=1))
