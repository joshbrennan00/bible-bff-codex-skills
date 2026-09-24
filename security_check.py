"""Scan tracked working-tree files and reachable commit blobs; no network access."""
import pathlib,re,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
patterns=[rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{20,}',rb'github_pat_[A-Za-z0-9_]{20,}',rb'AIza[0-9A-Za-z_-]{30,}',rb'sk-[A-Za-z0-9_-]{24,}',rb'"private_key"\s*:\s*"[^"\s]+',rb'(?:/Users/|/home/)[A-Za-z0-9_.-]+/',rb'https://drive\.google\.com/(?:file/d|drive/folders)/[A-Za-z0-9_-]{15,}']
allowed={'.md','.py','.cjs','.yaml','.yml','.example'}
problems=[]
def scan(label,data):
 if b'\x00' in data:problems.append((label,'binary content'))
 for p in patterns:
  if re.search(p,data):problems.append((label,'sensitive pattern'))
for raw in git('ls-files','-z').split(b'\0'):
 if not raw:continue
 rel=raw.decode();p=root/rel
 if p.is_symlink():problems.append((rel,'symlink'));continue
 if p.name not in {'.gitignore','.env.example','LICENSE'} and p.suffix not in allowed:problems.append((rel,'unexpected file type'))
 if any(part in {'work','private','recordings','receipts','.auth'} for part in p.relative_to(root).parts):problems.append((rel,'private directory'))
 if p.name.startswith('.env') and p.name!='.env.example':problems.append((rel,'environment file'))
 scan(rel,p.read_bytes())
try:
 objects=git('rev-list','--objects','--all').splitlines()
except subprocess.CalledProcessError:objects=[]
for row in objects:
 oid=row.split(b' ',1)[0].decode()
 if git('cat-file','-t',oid).strip()==b'blob':scan('history:'+oid,git('cat-file','blob',oid))
for label,reason in problems:print(label,reason)
print('PASS: no configured secret patterns found' if not problems else 'FAIL: inspect findings before publication')
sys.exit(bool(problems))
