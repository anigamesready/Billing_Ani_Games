#!/usr/bin/env python3
"""Narrow V12 patch for the locked Ani-Games Android WebView source."""
import re,sys
from pathlib import Path
P="https://wzkjpycjizexxcxrfdvr.supabase.co"
PK="sb_publishable_DobdCrOd43-vluON5gV7hg_6Js2Ea5V"
B="https://xcdbipgsvohesxhxydep.supabase.co"
BK="sb_publishable_FjhnRZeXPnomlGRw75YLxw_d46R2Lag"
ROUTE = r'''
// Ani-Games V12: read-only dual-project route validation; never switches route.
const DB_ROUTE_CONFIG=Object.freeze({
 primary:{url:"https://wzkjpycjizexxcxrfdvr.supabase.co",key:"sb_publishable_DobdCrOd43-vluON5gV7hg_6Js2Ea5V",ref:"wzkjpycjizexxcxrfdvr"},
 backup:{url:"https://xcdbipgsvohesxhxydep.supabase.co",key:"sb_publishable_FjhnRZeXPnomlGRw75YLxw_d46R2Lag",ref:"xcdbipgsvohesxhxydep"}
});
let dbRouteState=null;
function dbRouteNotice(t,ok=false){try{let e=document.getElementById("dbRouteNotice");if(!e){e=document.createElement("div");e.id="dbRouteNotice";e.style.cssText="position:fixed;z-index:99999;top:8px;left:8px;right:8px;padding:10px;border-radius:10px;font:600 12px/1.4 system-ui;overflow-wrap:anywhere";document.body.appendChild(e)}e.style.background=ok?"#123327":"#521c27";e.style.color="#fff";e.textContent=t;if(ok)setTimeout(()=>e.isConnected&&e.remove(),3500)}catch(_){}}
const dbRouteReady=(async()=>{
 async function readRoute(profile){const c=DB_ROUTE_CONFIG[profile];const probe=supabase.createClient(c.url,c.key,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});const {data:raw,error}=await probe.schema("api").rpc("db_route_get");const d=Array.isArray(raw)?raw[0]:raw;if(error||!d||typeof d!=="object")throw new Error("DB_ROUTE_UNAVAILABLE:"+profile);if(d.local_profile!==profile||d.project_ref!==c.ref)throw new Error("DB_ROUTE_PROFILE_MISMATCH:"+profile);const epoch=Number(d.epoch);if(!Number.isSafeInteger(epoch)||epoch<1)throw new Error("DB_ROUTE_EPOCH_INVALID:"+profile);if(!["primary","backup"].includes(d.active_target))throw new Error("DB_ROUTE_TARGET_INVALID:"+profile);return{target:d.active_target,epoch}}
 const [p,b]=await Promise.all([readRoute("primary"),readRoute("backup")]);if(p.target!==b.target||p.epoch!==b.epoch)throw new Error("DB_ROUTE_CONFLICT: route records differ; actions blocked");const c=DB_ROUTE_CONFIG[p.target];SB_URL=c.url;SB_KEY=c.key;if(typeof SB_FUNCTION_URL!=="undefined")SB_FUNCTION_URL=c.url+"/functions/v1/ani-games-api";sb=supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});dbRouteState={target:p.target,epoch:p.epoch,project_ref:c.ref,checked_at:new Date().toISOString()};window.aniGamesDbRoute=dbRouteState;const host=document.querySelector(".userbox")||document.querySelector(".top .row")||document.querySelector(".secure")?.parentElement||document.querySelector(".topbar");if(host&&!document.getElementById("dbRouteBadge")){const e=document.createElement("span");e.id="dbRouteBadge";e.className="pill";e.textContent="DB "+p.target.toUpperCase()+" · E"+p.epoch;host.appendChild(e)}dbRouteNotice("Database siap: "+p.target.toUpperCase()+" · epoch "+p.epoch,true);return dbRouteState
})().catch(e=>{dbRouteNotice("AKSES DATABASE DIBLOKIR — "+String(e?.message||e)+". Tidak ada perintah dikirim.");console.error("Ani-Games V12 route blocked",e);throw e});
dbRouteReady.catch(()=>{});
'''
CSS_ADMIN = r'''
/* Ani-Games V12 handset fit: presentation only */
@media(max-width:700px){html,body{width:100%;max-width:100%;min-width:0;overflow-x:hidden}body{padding-bottom:calc(12px + env(safe-area-inset-bottom))}.wrap,.shell,.content,.section,.card,.top,.row,.toolbar,.field{min-width:0;max-width:100%}.wrap{width:100%;padding:10px}.shell{grid-template-columns:minmax(0,1fr);gap:9px}.top{gap:9px;align-items:flex-start;flex-wrap:wrap}.top>div,.top>.row{min-width:0;max-width:100%}#remote-target-bar .top{display:grid;grid-template-columns:minmax(0,1fr)}#remote-target-bar .top>.row{display:grid;grid-template-columns:minmax(0,1fr);width:100%}#globalDeviceSelect{width:100%;min-width:0;max-width:100%}.grid,.grid6{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.cards2,.cards3{grid-template-columns:minmax(0,1fr);gap:9px}.toolbar{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}.toolbar>*{width:100%;min-width:0;max-width:100%}input,select,textarea,button{max-width:100%;min-width:0}.table-wrap{width:100%;max-width:100%;min-width:0;overflow-x:auto;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}.modal{padding:10px}.modal-box{width:100%;max-width:100%;max-height:calc(100dvh - 20px);overflow:auto;padding:13px}.field input,.field select{width:100%;min-width:0}.stat{overflow-wrap:anywhere;font-size:clamp(19px,6vw,26px)}}
@media(max-width:420px){.wrap{padding:8px}.card{padding:11px;border-radius:14px}.brand{font-size:20px;overflow-wrap:anywhere}.grid,.grid6{grid-template-columns:minmax(0,1fr);gap:7px}.toolbar{grid-template-columns:minmax(0,1fr)}.nav{grid-template-columns:repeat(2,minmax(0,1fr))}.pill{max-width:100%;overflow-wrap:anywhere}.chartbox{height:230px}}
@media(max-width:350px){.wrap{padding:6px}.card{padding:9px}.brand{font-size:18px}.modal-box{padding:10px}}
'''
CSS_CONTROL = r'''
/* Ani-Games V12 handset fit: presentation only */
@media(max-width:640px){html,body{width:100%;max-width:100%;min-width:0;overflow-x:hidden}body{padding-bottom:calc(12px + env(safe-area-inset-bottom))}.wrap{width:100%;max-width:100%;padding:10px}.top{display:flex;flex-direction:column;align-items:stretch;gap:9px}.top>div,.row,.section,.card,.field{min-width:0;max-width:100%}.top .row{width:100%;display:grid;grid-template-columns:minmax(0,1fr);gap:7px}#deviceSelect{width:100%;max-width:100%;min-width:0}.grid,.stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.pc-detail,.pc-list,.pcbar,.form-grid{grid-template-columns:minmax(0,1fr);gap:9px}.nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;overflow:visible}.nav button{min-width:0;white-space:normal;overflow-wrap:anywhere;line-height:1.25;padding:10px 6px}.section-head{align-items:stretch;flex-wrap:wrap}.section-head>.btn{width:100%;min-width:0}.controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}.controls>*{min-width:0;max-width:100%;width:100%}.table-wrap,.table-scroll{width:100%;max-width:100%;min-width:0;overflow-x:auto;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}.table{min-width:610px}input,select,textarea,button{max-width:100%;min-width:0}.modal{padding:10px}.modal-box{width:100%;max-width:100%;max-height:calc(100dvh - 20px);overflow:auto;padding:13px}.card{padding:12px;border-radius:14px}.brand{font-size:clamp(19px,5.6vw,23px);overflow-wrap:anywhere}}
@media(max-width:360px){.wrap{padding:8px}.grid,.stats{grid-template-columns:minmax(0,1fr)}.nav{grid-template-columns:repeat(2,minmax(0,1fr))}.stat{font-size:22px}.card{padding:10px}}
'''
def css(path, fragment, marker):
 t=path.read_text()
 if marker not in t:
  i=t.lower().rfind('</style>')
  if i<0: raise SystemExit('style tag missing: '+str(path))
  path.write_text(t[:i]+fragment+'\n'+t[i:])
def insert_route(path, kind):
 t=path.read_text()
 if 'const DB_ROUTE_CONFIG' in t:
  if 'DB_ROUTE_CONFLICT' in t and 'await dbRouteReady' in t:return
  raise SystemExit('partial route patch exists: '+str(path))
 if kind=='login':
  for old,new in [(f"const SB_URL='{P}';",f"let SB_URL='{P}';"),(f"const SB_KEY='{PK}';",f"let SB_KEY='{PK}';")]:
   if t.count(old)!=1:raise SystemExit('login constant mismatch: '+old)
   t=t.replace(old,new,1)
  pat=r"const sb=supabase\.createClient\(SB_URL,SB_KEY,(\{auth:\{[^\n]*?\}\})\);"
 elif kind=='control':
  old=f"const SB_URL='{P}',SB_KEY='{PK}',SESSION_KEY='ani_games_billing_control_session_v1';"
  new=f"let SB_URL='{P}',SB_KEY='{PK}';const SESSION_KEY='ani_games_billing_control_session_v1';"
  if t.count(old)!=1:raise SystemExit('control constants mismatch')
  t=t.replace(old,new,1)
  pat=r"const sb=supabase\.createClient\(SB_URL,SB_KEY,(\{auth:\{[^\n]*?\}\})\);"
 elif kind=='admin':
  old=f"const SB_URL='{P}',SB_KEY='{PK}',SB_FUNCTION_URL=SB_URL+'/functions/v1/ani-games-api',sb=supabase.createClient(SB_URL,SB_KEY);"
  new=f"let SB_URL='{P}',SB_KEY='{PK}',SB_FUNCTION_URL=SB_URL+'/functions/v1/ani-games-api',sb=supabase.createClient(SB_URL,SB_KEY);"
  if t.count(old)!=1:raise SystemExit('admin constants mismatch')
  t=t.replace(old,new,1)
  t=t.replace(new,new+ROUTE,1)
  rpc="async function rpc(name,args={}){const r=await sb.schema('api').rpc(name,args);"
  if t.count(rpc)!=1:raise SystemExit('admin rpc mismatch')
  t=t.replace(rpc,"async function rpc(name,args={}){await dbRouteReady;const r=await sb.schema('api').rpc(name,args);",1)
  for sig,rep in [("async function login(){","async function login(){await dbRouteReady;"),("async function signup(){","async function signup(){await dbRouteReady;"),("async function resetPassword(){","async function resetPassword(){await dbRouteReady;"),("async function boot(){const r=await sb.auth.getSession();","async function boot(){await dbRouteReady;const r=await sb.auth.getSession();")]:
   if t.count(sig)!=1:raise SystemExit('admin function signature mismatch: '+sig)
   t=t.replace(sig,rep,1)
  tail="$('from').value=new Date(Date.now()-29*864e5).toISOString().slice(0,10);$('to').value=new Date().toISOString().slice(0,10);sb.auth.onAuthStateChange(()=>setTimeout(boot,0));boot();setInterval(()=>{if(session&&currentOrg)loadDevices()},20000);"
  rep="$('from').value=new Date(Date.now()-29*864e5).toISOString().slice(0,10);$('to').value=new Date().toISOString().slice(0,10);dbRouteReady.then(()=>{sb.auth.onAuthStateChange(()=>setTimeout(()=>boot().catch(e=>msg(e.message||'Gagal memuat admin.',true)),0));return boot()}).catch(e=>msg('Akses DB diblokir: '+(e.message||e),true));setInterval(()=>{if(session&&currentOrg)loadDevices().catch(()=>{})},20000);"
  if t.count(tail)!=1:raise SystemExit('admin auth tail mismatch')
  t=t.replace(tail,rep,1)
  path.write_text(t);return
 else:
  m=re.search(pat,t)
  if not m:raise SystemExit('client init mismatch: '+str(path))
  t=t[:m.start()]+f"let sb=supabase.createClient(SB_URL,SB_KEY,{m.group(1)});"+ROUTE+t[m.end():]
  rpc="async function rpc(name,args={}){const r=await sb.schema('api').rpc(name,args);"
  if t.count(rpc)!=1:raise SystemExit('rpc signature mismatch: '+str(path))
  t=t.replace(rpc,"async function rpc(name,args={}){await dbRouteReady;const r=await sb.schema('api').rpc(name,args);",1)
  if kind=='login':
   old="catch(_){sessionStorage.removeItem(SESSION_KEY)}})();"
   if t.count(old)!=1:raise SystemExit('session restore catch mismatch')
   t=t.replace(old,"catch(e){if(String(e?.message||e).startsWith('DB_ROUTE_'))return;sessionStorage.removeItem(SESSION_KEY)}})();",1)
  else:
   old="async function boot(){token=sessionStorage"
   if t.count(old)!=1:raise SystemExit('control boot signature mismatch')
   t=t.replace(old,"async function boot(){await dbRouteReady;token=sessionStorage",1)
 path.write_text(t)
def patch_cloud(path):
 t=path.read_text()
 if 'V12_DUAL_DB_ROUTE' in t:return
 old=f"const CLOUD_KEY='billing_v11_cloud_config',OUTBOX_KEY='billing_v11_outbox',API_BASE='{P}/functions/v1/ani-games-api',API_KEY='{PK}',CLIENT_KEY='billing_v11_client_id',APP='V11.29.1-SUPABASE-DIRECT-APIKEY-FIX';"
 new=f"""const CLOUD_KEY='billing_v11_cloud_config',OUTBOX_KEY='billing_v11_outbox',CLIENT_KEY='billing_v11_client_id',APP='V12.0.0-SUPABASE-DUAL-DB';
  // V12_DUAL_DB_ROUTE: public keys only; read-only preflight.
  const DB_ROUTE_CONFIG=Object.freeze({{primary:{{url:'{P}',key:'{PK}',ref:'wzkjpycjizexxcxrfdvr'}},backup:{{url:'{B}',key:'{BK}',ref:'xcdbipgsvohesxhxydep'}}}});
  let API_BASE='{P}/functions/v1/ani-games-api',API_KEY='{PK}',dbRouteState=null;
  const DB_ROUTE_READY=(async()=>{{
    async function readRoute(profile){{const c=DB_ROUTE_CONFIG[profile];const r=await fetch(c.url+'/rest/v1/rpc/db_route_get',{{method:'POST',headers:{{'content-type':'application/json','apikey':c.key,'authorization':'Bearer '+c.key,'content-profile':'api','accept-profile':'api'}},body:'{{}}'}});const raw=await r.json().catch(()=>null),d=Array.isArray(raw)?raw[0]:raw;if(!r.ok||!d||typeof d!=='object')throw new Error('DB_ROUTE_UNAVAILABLE:'+profile);if(d.local_profile!==profile||d.project_ref!==c.ref)throw new Error('DB_ROUTE_PROFILE_MISMATCH:'+profile);const epoch=Number(d.epoch);if(!Number.isSafeInteger(epoch)||epoch<1)throw new Error('DB_ROUTE_EPOCH_INVALID:'+profile);if(!['primary','backup'].includes(d.active_target))throw new Error('DB_ROUTE_TARGET_INVALID:'+profile);return{{target:d.active_target,epoch}}}}
    const [p,b]=await Promise.all([readRoute('primary'),readRoute('backup')]);if(p.target!==b.target||p.epoch!==b.epoch)throw new Error('DB_ROUTE_CONFLICT: database route records differ');const c=DB_ROUTE_CONFIG[p.target];API_BASE=c.url+'/functions/v1/ani-games-api';API_KEY=c.key;dbRouteState={{target:p.target,epoch:p.epoch,project_ref:c.ref,checked_at:new Date().toISOString()}};window.v11DbRouteState=dbRouteState;return dbRouteState;
  }})();DB_ROUTE_READY.catch(()=>{{}});"""
 if t.count(old)!=1:raise SystemExit('v11-cloud header mismatch')
 t=t.replace(old,new,1)
 sig="async function request(path,body){const r=await fetch(API_BASE+path,"
 if t.count(sig)!=1:raise SystemExit('cloud request signature mismatch')
 t=t.replace(sig,"async function request(path,body){await DB_ROUTE_READY;const r=await fetch(API_BASE+path,",1)
 path.write_text(t)
def main():
 if len(sys.argv)!=2:raise SystemExit('usage: patch_android_v12.py <android-project-root>')
 root=Path(sys.argv[1]).resolve();web=root/'app/src/main/assets/web';gradle=root/'app/build.gradle'
 if not web.is_dir() or not gradle.is_file():raise SystemExit('Android project root invalid')
 if "versionName '11.29.1'" not in gradle.read_text():raise SystemExit('expected locked V11.29.1 source; refusing unknown baseline')
 for f,k in [('index.html','login'),('admin-control.html','control'),('admin.html','admin')]:insert_route(web/f,k)
 patch_cloud(web/'v11-cloud.js')
 css(web/'admin.html',CSS_ADMIN,'Ani-Games V12 handset fit')
 css(web/'admin-control.html',CSS_CONTROL,'Ani-Games V12 handset fit')
 css(web/'index.html',"\n/* Ani-Games V12 login sizing */\nhtml,body{width:100%;max-width:100%;min-width:0;overflow-x:hidden}main.card{width:min(430px,calc(100vw - 24px));max-width:100%;min-width:0}input,button{max-width:100%;min-width:0}@media(max-width:360px){main.card{padding:14px}.brand{font-size:20px}}\n",'Ani-Games V12 login sizing')
 t=gradle.read_text();t,n=re.subn(r'versionCode\s+\d+','versionCode 31',t,count=1);t,n2=re.subn(r"versionName\s+'[^']+'","versionName '12.0.0'",t,count=1)
 if n!=1 or n2!=1:raise SystemExit('Gradle version replacement failed')
 gradle.write_text(t)
 print('V12 route guard and phone layout patch applied; no DB route writes performed.')
if __name__=='__main__':main()
