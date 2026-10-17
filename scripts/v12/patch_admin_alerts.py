#!/usr/bin/env python3
"""Patch isolated Admin APK with rental-alerts and DB2 pairing diagnostics."""
import re
import sys
from pathlib import Path

ALERT_JS = r"""
(function v12InstallRentalAlerts(){
  if(window.__v12RentalAlertsInstalled)return;
  window.__v12RentalAlertsInstalled=true;
  const scopeKey=()=>String(typeof DB_TARGET==='undefined'?'primary':DB_TARGET)+':'+String(currentOrg&&currentOrg.id||'no-org');
  let activeScope=scopeKey(),deviceReady=false,deviceSnapshots=new Map(),accountReady=false,accountSnapshots=new Map(),accountBusy=false;
  const queue=[],seen=new Set(),recent=new Map(),seenKey='ani_games_admin_rental_alerts_v1:'+activeScope;
  try{JSON.parse(sessionStorage.getItem(seenKey)||'[]').slice(-250).forEach(x=>seen.add(x))}catch(_){}
  const style=document.createElement('style');style.id='v12RentalAlertStyles';
  style.textContent='#v12RentalAlertShade{position:fixed;inset:0;z-index:2147483000;background:rgba(2,8,23,.8);display:flex;align-items:center;justify-content:center;padding:18px;box-sizing:border-box}#v12RentalAlertCard{width:min(520px,100%);box-sizing:border-box;border:2px solid #ff5d67;border-radius:20px;background:#111827;color:#fff;padding:22px;box-shadow:0 24px 90px rgba(0,0,0,.7);font-family:system-ui,sans-serif}#v12RentalAlertEyebrow{font-size:12px;font-weight:900;letter-spacing:1.5px;color:#ff7e86;margin-bottom:8px}#v12RentalAlertTitle{font-size:clamp(22px,5vw,30px);font-weight:900;line-height:1.15;margin:0 0 12px}#v12RentalAlertBody{font-size:16px;line-height:1.55;overflow-wrap:anywhere;white-space:pre-wrap;color:#f3f4f6}#v12RentalAlertTime{font-size:12px;color:#aeb8ca;margin-top:12px}#v12RentalAlertAck{border:0;border-radius:12px;background:#ff525d;color:#18080a;font-weight:900;font-size:15px;padding:14px 18px;width:100%;margin-top:20px;min-height:50px}';
  document.head.appendChild(style);
  const shade=document.createElement('div');shade.id='v12RentalAlertShade';shade.style.display='none';shade.setAttribute('role','alertdialog');shade.setAttribute('aria-modal','true');
  shade.innerHTML='<div id="v12RentalAlertCard"><div id="v12RentalAlertEyebrow">ANI GAMES • NOTIFIKASI RENTAL</div><div id="v12RentalAlertTitle">SESI RENTAL BERAKHIR</div><div id="v12RentalAlertBody"></div><div id="v12RentalAlertTime"></div><button id="v12RentalAlertAck" type="button">SUDAH SAYA CEK • MATIKAN ALARM</button></div>';
  document.body.appendChild(shade);
  const titleEl=document.getElementById('v12RentalAlertTitle'),bodyEl=document.getElementById('v12RentalAlertBody'),timeEl=document.getElementById('v12RentalAlertTime'),ackEl=document.getElementById('v12RentalAlertAck');
  function persist(){try{sessionStorage.setItem(seenKey,JSON.stringify(Array.from(seen).slice(-250)))}catch(_){}}
  function nativeNotify(item){try{const b=window.AniGamesAdminNative;if(b&&typeof b.notifyRentalEvent==='function')b.notifyRentalEvent(item.title,item.body,item.id)}catch(e){console.warn('Native rental alert failed',e)}}
  function render(){const item=queue[0];if(!item){shade.style.display='none';return}titleEl.textContent=item.title;bodyEl.textContent=item.body;timeEl.textContent=item.time+(queue.length>1?' • '+queue.length+' alert belum diperiksa':'');shade.style.display='flex'}
  function raise(type,key,code,pc,extra){
    const scope=scopeKey();if(scope!==activeScope){activeScope=scope;deviceReady=false;deviceSnapshots=new Map();accountReady=false;accountSnapshots=new Map()}
    const now=Date.now(),dedupe=scope+'|'+key+'|'+type;
    if(now-(recent.get(dedupe)||0)<45000||seen.has(dedupe))return;
    recent.set(dedupe,now);seen.add(dedupe);persist();
    const db=typeof DB_TARGET!=='undefined'&&DB_TARGET==='backup'?'DB2':'DB1';
    const title=type==='expired'?'WAKTU RENTAL HABIS':type==='stopped'?'SESI RENTAL DIHENTIKAN':'SESI RENTAL BERAKHIR';
    const lines=[];if(code)lines.push('Kode rental: '+code);if(pc)lines.push('PC: '+pc);lines.push('Database aktif: '+db);if(extra)lines.push(extra);lines.push('Periksa status PC dan riwayat rental untuk memastikan kondisi terakhir.');
    const item={id:dedupe+':'+now,title,body:lines.join('\n'),time:new Date(now).toLocaleString('id-ID')};queue.push(item);nativeNotify(item);if(queue.length===1)render();
  }
  ackEl.addEventListener('click',function(){const item=queue.shift();try{const b=window.AniGamesAdminNative;if(b&&typeof b.acknowledgeRentalEvent==='function'&&item)b.acknowledgeRentalEvent(item.id)}catch(_){}render();if(queue.length)nativeNotify(queue[0])});
  function snap(d){const m=d&&d.metadata||{},a=String(m.activeCode||'').trim(),p=String(m.pausedCode||'').trim(),raw=a?m.activeRemainingSeconds:m.pausedRemainingSeconds,n=Number(raw);return{id:String(d&&d.id||''),name:String(d&&(d.device_name||d.client_id)||'PC tidak dikenal'),status:String(d&&d.uiStatus||''),code:a||p,paused:!!p&&!a,remaining:Number.isFinite(n)?n:null}}
  if(typeof loadDevices==='function'){
    const original=loadDevices;
    loadDevices=async function(){const result=await original.apply(this,arguments);if(!session||!currentOrg||!Array.isArray(devicesCache))return result;
      const s=scopeKey();if(s!==activeScope){activeScope=s;deviceReady=false;deviceSnapshots=new Map();accountReady=false;accountSnapshots=new Map()}
      const next=new Map();devicesCache.forEach(d=>{const x=snap(d);if(x.id)next.set(x.id,x)});
      if(!deviceReady){deviceSnapshots=next;deviceReady=true;return result}
      for(const [id,before] of deviceSnapshots.entries()){const after=next.get(id);if(!after||after.status!=='online'||!before.code)continue;
        if(after.code!==before.code){const type=before.remaining!==null&&before.remaining<=0?'expired':'ended';raise(type,'device:'+id+':'+before.code,before.code,before.name,after.code?'Sesi sebelumnya berakhir saat PC melaporkan kode rental baru.':(before.paused?'Sesi jeda tidak lagi tercatat aktif.':'PC tidak lagi melaporkan sesi rental aktif.'))}
        else if(before.remaining!==null&&before.remaining>0&&after.remaining!==null&&after.remaining<=0)raise('expired','device:'+id+':'+before.code,before.code,before.name,'Sisa waktu pada timer PC mencapai nol.');
      }
      deviceSnapshots=next;return result
    }
  }
  const terminal=new Set(['expired','stopped','completed','ended','cancelled','canceled','finished','terminated','ended_by_admin','closed']);
  const active=new Set(['active','running','in_use','in-use','using','paused','rental','playing']);
  async function pollAccounts(){if(accountBusy||!session||!currentOrg||!sb)return;accountBusy=true;try{
      const q=await sb.from('rental_accounts').select('id,code,status,expiry_at,device_id,client_label,created_at').eq('org_id',currentOrg.id).order('created_at',{ascending:false}).limit(200);
      if(q.error||!Array.isArray(q.data))return;
      const s=scopeKey();if(s!==activeScope){activeScope=s;deviceReady=false;deviceSnapshots=new Map();accountReady=false;accountSnapshots=new Map()}
      const next=new Map();q.data.forEach(r=>{if(r.id)next.set(String(r.id),{id:String(r.id),code:String(r.code||''),status:String(r.status||'').toLowerCase().trim(),expiry:r.expiry_at?new Date(r.expiry_at).getTime():null,pc:String(r.client_label||r.device_id||'')})});
      if(!accountReady){accountSnapshots=next;accountReady=true;return}
      const now=Date.now();for(const [id,b] of accountSnapshots.entries()){const a=next.get(id);if(!a)continue;
        if(active.has(b.status)&&terminal.has(a.status)&&b.status!==a.status)raise(a.status==='expired'?'expired':'stopped','account:'+id+':'+a.status,a.code,a.pc,'Status rental berubah dari '+b.status+' menjadi '+a.status+'.');
        else if(active.has(b.status)&&b.expiry&&b.expiry>now&&a.expiry&&a.expiry<=now)raise('expired','account:'+id+':expiry',a.code,a.pc,'Waktu expiry rental telah terlewati.')
      }accountSnapshots=next;
    }catch(e){console.debug('Rental alert status check skipped:',e&&e.message||e)}finally{accountBusy=false}}
  setInterval(pollAccounts,12000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)pollAccounts()});setTimeout(pollAccounts,2500);
  window.v12RentalAlertDiagnostics=()=>({database:typeof DB_TARGET==='undefined'?'unknown':DB_TARGET,org:currentOrg&&currentOrg.id||null,pending:queue.length,deviceSnapshots:deviceSnapshots.size,accountSnapshots:accountSnapshots.size});
})();
"""

def patch_html(web: Path):
    path=web/'admin.html'
    text=path.read_text(encoding='utf-8')
    if 'v12InstallRentalAlerts' in text:
        print('Admin rental alerts already installed.')
        return
    matches=[m for m in re.finditer(r'<script\b([^>]*)>(.*?)</script\s*>',text,re.I|re.S)
             if not re.search(r'\bsrc\s*=',m.group(1),re.I) and m.group(2).strip()]
    if not matches: raise SystemExit('No inline JavaScript block found in admin.html')
    target=max(matches,key=lambda m:len(m.group(2)))
    js=target.group(2)
    needle='Masukkan kode ini di Panel Admin PC V11.</div>'
    if needle in js:
        db_label=chr(36)+"{DB_TARGET==='backup'?'DB2 • Cadangan':'DB1 • Utama'}"
        js=js.replace(needle,'Masukkan kode ini di Panel Admin PC V11.<br>Database: '+db_label+'</div>',1)
    old="async function rpc(name,args={}){const r=await sb.schema('api').rpc(name,args);if(r.error)throw r.error;return r.data}"
    new=("async function rpc(name,args={}){const r=await sb.schema('api').rpc(name,args);"
         "if(r.error){if(name==='create_enrollment'&&DB_TARGET==='backup')throw new Error("
         "'Pairing DB2 tidak tersedia: pastikan RPC api.create_enrollment, tabel/enrollment pairing, "
         "dan akun Owner sudah disiapkan di DB2. Tidak dialihkan diam-diam ke DB1 agar kode tidak masuk "
         "ke tenant/database yang salah. Detail: '+(r.error.message||r.error));throw r.error;}return r.data}")
    if old in js: js=js.replace(old,new,1)
    text=text[:target.start(2)]+js+'\n'+ALERT_JS+text[target.end(2):]
    path.write_text(text,encoding='utf-8')
    print('Patched DB1/DB2-aware pairing status and rental lifecycle alert listeners.')

def patch_android(root: Path):
    activities=list((root/'app/src/main/java').rglob('MainActivity.java'))
    if len(activities)!=1: raise SystemExit('Expected one MainActivity.java, got '+str(len(activities)))
    activity=activities[0]
    old=activity.read_text(encoding='utf-8',errors='replace')
    m=re.search(r'^\s*package\s+([A-Za-z0-9_.]+)\s*;',old,re.M)
    if not m: raise SystemExit('Could not identify MainActivity package')
    package=m.group(1)
    if 'notifyRentalEvent' not in old or 'AniGamesAdminNative' not in old:
        java=r'''PACKAGE_LINE

import android.Manifest;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.view.Window;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private static final String CHANNEL_ID = "ani_games_rental_alarm_v1";
    private static final int NOTIFICATION_PERMISSION_REQUEST = 5101;
    private WebView web;
    private Ringtone alarmRingtone;
    private NotificationManager notificationManager;
    private String activeAlarmId = "";

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        notificationManager = (NotificationManager)getSystemService(Context.NOTIFICATION_SERVICE);
        createRentalAlertChannel();
        web = new WebView(this);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setLoadWithOverviewMode(false);
        s.setUseWideViewPort(false);
        s.setTextZoom(100);
        s.setMediaPlaybackRequiresUserGesture(true);
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient());
        web.addJavascriptInterface(new AdminNotificationBridge(), "AniGamesAdminNative");
        web.loadUrl("file:///android_asset/web/admin.html");
        requestNotificationPermissionIfNeeded();
    }

    private void createRentalAlertChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Uri alarm = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, "Peringatan sesi rental", NotificationManager.IMPORTANCE_HIGH);
            channel.setDescription("Alert dan getar ketika sesi rental PC habis atau dihentikan.");
            channel.enableVibration(true);
            channel.setVibrationPattern(new long[]{0,800,250,800,250,1200});
            if (alarm != null) {
                AudioAttributes audio = new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build();
                channel.setSound(alarm,audio);
            }
            if (notificationManager != null) notificationManager.createNotificationChannel(channel);
        }
    }

    private void requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= 33 && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, NOTIFICATION_PERMISSION_REQUEST);
        }
    }

    private int notificationId(String eventId) {
        int hash = eventId == null ? (int)System.currentTimeMillis() : eventId.hashCode();
        return 8000 + ((hash & 0x7fffffff) % 100000);
    }

    private void startAlarm(String eventId) {
        if (eventId != null && eventId.equals(activeAlarmId) && alarmRingtone != null && alarmRingtone.isPlaying()) return;
        stopAlarm(); activeAlarmId = eventId == null ? "" : eventId;
        try {
            Uri uri=RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
            if(uri==null)uri=RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            if(uri!=null){alarmRingtone=RingtoneManager.getRingtone(getApplicationContext(),uri);
                if(alarmRingtone!=null){if(Build.VERSION.SDK_INT>=Build.VERSION_CODES.P)alarmRingtone.setLooping(true);alarmRingtone.play();}}
        } catch(Exception e){android.util.Log.w("AniGamesAdmin","Unable to start rental alarm",e);}
    }

    private void stopAlarm() {
        try { if(alarmRingtone!=null&&alarmRingtone.isPlaying())alarmRingtone.stop(); } catch(Exception ignored) {}
        alarmRingtone=null;activeAlarmId="";
    }

    private void showRentalNotification(String title,String body,String eventId) {
        requestNotificationPermissionIfNeeded();
        if(Build.VERSION.SDK_INT>=33&&checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)!=PackageManager.PERMISSION_GRANTED)return;
        if(notificationManager==null)return;
        int id=notificationId(eventId);
        Intent open=new Intent(this,MainActivity.class);open.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pending=PendingIntent.getActivity(this,id,open,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
        String safeTitle=title==null?"Sesi rental berakhir":title;
        String safeBody=body==null?"Periksa status sesi rental PC.":body;
        Notification.Builder builder=Build.VERSION.SDK_INT>=Build.VERSION_CODES.O?new Notification.Builder(this,CHANNEL_ID):new Notification.Builder(this);
        builder.setSmallIcon(getApplicationInfo().icon).setContentTitle(safeTitle).setContentText(safeBody)
            .setStyle(new Notification.BigTextStyle().bigText(safeBody)).setCategory(Notification.CATEGORY_ALARM)
            .setPriority(Notification.PRIORITY_MAX).setVisibility(Notification.VISIBILITY_PUBLIC).setContentIntent(pending)
            .setAutoCancel(false).setOngoing(true).setVibrate(new long[]{0,800,250,800,250,1200});
        if(Build.VERSION.SDK_INT<Build.VERSION_CODES.O){Uri alarm=RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);if(alarm!=null)builder.setSound(alarm);}
        notificationManager.notify(id,builder.build());
        startAlarm(eventId);
    }

    private void acknowledgeRentalNotification(String eventId) {
        if(notificationManager!=null&&eventId!=null&&!eventId.isEmpty())notificationManager.cancel(notificationId(eventId));
        stopAlarm();
    }

    private final class AdminNotificationBridge {
        @JavascriptInterface public void notifyRentalEvent(final String title,final String body,final String eventId) {
            runOnUiThread(()->showRentalNotification(title,body,eventId));
        }
        @JavascriptInterface public void acknowledgeRentalEvent(final String eventId) {
            runOnUiThread(()->acknowledgeRentalNotification(eventId));
        }
    }

    @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] grantResults) {
        super.onRequestPermissionsResult(requestCode,permissions,grantResults);
        if(requestCode==NOTIFICATION_PERMISSION_REQUEST&&grantResults.length>0&&grantResults[0]==PackageManager.PERMISSION_GRANTED)createRentalAlertChannel();
    }

    @Override public void onBackPressed() {
        if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();
    }
    @Override protected void onDestroy() {
        stopAlarm();
        if(web!=null){web.removeJavascriptInterface("AniGamesAdminNative");web.destroy();}
        super.onDestroy();
    }
}
'''
        activity.write_text(java.replace('PACKAGE_LINE','package '+package+';'),encoding='utf-8')
        print('Installed Android native high-priority alert notifications and alarm bridge.')
    manifest=root/'app/src/main/AndroidManifest.xml'
    if not manifest.is_file():raise SystemExit('AndroidManifest.xml is missing')
    xml=manifest.read_text(encoding='utf-8',errors='replace')
    if 'android.permission.POST_NOTIFICATIONS' not in xml:
        marker='<uses-permission android:name="android.permission.INTERNET" />'
        if marker not in xml:raise SystemExit('Manifest INTERNET permission marker not found')
        xml=xml.replace(marker,marker+'\n    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',1)
        manifest.write_text(xml,encoding='utf-8')
    print('Added Android notification permission.')

def main():
    if len(sys.argv)!=3:raise SystemExit('usage: patch_admin_alerts.py <web-assets-dir> <android-project-root>')
    web,root=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
    if not (web/'admin.html').is_file():raise SystemExit('admin.html missing in '+str(web))
    patch_html(web);patch_android(root)

if __name__=='__main__':main()
