"""Offline title proposals. Never produces approval or performs publication."""
import argparse, collections, difflib, json, re, unicodedata
from pathlib import Path
from urllib.parse import unquote

def norm(t, noise=()):
    t=unicodedata.normalize('NFKD',unquote(t)).encode('ascii','ignore').decode().lower()
    t=re.sub(r'\.(mp3|wav|m4a|mp4|mov)$','',t)
    t=re.sub(r'esv\d.*$','',t)
    t=re.sub(r'\b20\d\d[-_ ]\d\d[-_ ]\d\d',' ',t)
    t=t.replace('&',' and ').replace('_',' ').replace("'",'')
    t=re.sub(r'[^a-z0-9]+',' ',t)
    for n in sorted(noise,key=len,reverse=True):
        n=re.sub(r'[^a-z0-9]+',' ',n.lower()).strip()
        if n:t=re.sub(r'\b'+re.escape(n)+r'\b',' ',t)
    return re.sub(r'\s+',' ',t).strip()

class Matcher:
    def __init__(self,catalog,noise=()):
        self.noise=noise;self.aliases=collections.defaultdict(set)
        for s in catalog:
            for title in [s['title'],*s.get('aliases',[])]:
                n=norm(title,noise)
                if n:self.aliases[n].add(str(s['story_id']))
    def best(self,title):
        n=norm(title,self.noise);c=n.replace(' ','');a=self.aliases
        if n in a:
            if len(a[n])==1:return next(iter(a[n])),1.0,'exact',n
            return None,1.0,'ambiguous exact',n
        hits=[k for k in a if ((len(k.replace(' ',''))>=12 and k.replace(' ','') in c) or
              (len(k.replace(' ',''))>=8 and re.search(r'\b'+re.escape(k)+r'\b',n))) and len(a[k])==1]
        if hits:
            length=max(len(k.replace(' ','')) for k in hits)
            winners=[k for k in hits if len(k.replace(' ',''))==length]
            ids=set().union(*(a[k] for k in winners))
            if len(ids)==1:return next(iter(ids)),1.0,'title within filename',winners[0]
            return None,1.0,'ambiguous contained title',''
        scores={}
        for k in a:
            ck=k.replace(' ','')
            if abs(len(c)-len(ck))>max(len(c),len(ck))*.55:continue
            ratio=difflib.SequenceMatcher(None,c,ck).ratio()
            for sid in a[k]:
                if ratio>scores.get(sid,(0,''))[0]:scores[sid]=(ratio,k)
        rank=sorted(scores.items(),key=lambda x:x[1][0],reverse=True)
        if not rank:return None,0.0,'unmatched',''
        sid,(score,k)=rank[0];margin=score-(rank[1][1][0] if len(rank)>1 else 0)
        return sid,score,('close spelling' if score>=.93 and margin>=.08 else 'review'),k

def main():
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('files');p.add_argument('--out',required=True);p.add_argument('--noise')
    a=p.parse_args();m=Matcher(json.loads(Path(a.catalog).read_text()),json.loads(Path(a.noise).read_text()) if a.noise else [])
    out=[]
    for f in json.loads(Path(a.files).read_text()):
        sid,score,method,alias=m.best(f['title'])
        out.append({**f,'proposed_story_id':sid,'score':score,'method':method,'alias':alias,'approval':'pending'})
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x') as w:json.dump(out,w,indent=2,ensure_ascii=False)
if __name__=='__main__':main()
