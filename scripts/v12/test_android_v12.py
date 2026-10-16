#!/usr/bin/env python3
import re,sys
from pathlib import Path
a,b=map(lambda p:Path(p).resolve(),sys.argv[1:3]);x=a/'app/src/main/assets/web';y=b/'app/src/main/assets/web';fail=[]
for n in ('index.html','admin-control.html','admin.html','billing.html'):
 s=x.joinpath(n).read_text();t=y.joinpath(n).read_text()
 ids=lambda z:re.findall(r'\bid=["\']([^"\']+)',z)
 clicks=lambda z:re.findall(r'onclick\s*=\s*(["\'])(.*?)\1',z,re.I|re.S)
 if ids(s)!=ids(t):fail.append(n+' DOM ids changed')
 if clicks(s)!=clicks(t):fail.append(n+' inline handlers changed')
 print(n,': ids',len(ids(s)),'handlers',len(clicks(s)),'preserved=',ids(s)==ids(t) and clicks(s)==clicks(t))
for n in ('index.html','admin-control.html','admin.html'):
 t=y.joinpath(n).read_text()
 for z in ('DB_ROUTE_CONFIG','DB_ROUTE_CONFLICT','await dbRouteReady'):
  if z not in t:fail.append(n+' missing '+z)
 if 'service_role' in t.lower():fail.append(n+' has forbidden service key text')
if 'await DB_ROUTE_READY' not in y.joinpath('v11-cloud.js').read_text():fail.append('v11-cloud.js request not gated')
g=b/'app/build.gradle';t=g.read_text()
for z in ("versionCode 31","versionName '12.0.0'"):
 if z not in t:fail.append('version metadata missing '+z)
for n,z in [('index.html','Ani-Games V12 login sizing'),('admin.html','Ani-Games V12 handset fit'),('admin-control.html','Ani-Games V12 handset fit')]:
 if z not in y.joinpath(n).read_text():fail.append('responsive CSS missing '+n)
if fail: print('FAIL:',*fail,sep='\n- ');raise SystemExit(1)
print('PASS: no DOM ids/inline event handlers removed; DB route preflight and responsive styles present.')
