/* Run only inside the supported browser tool runtime; no network or credential access. */
function requireValue(ok,message){if(!ok)throw new Error(message);}
function field(snapshot,label){
  const lines=snapshot.split('\n');
  for(let i=0;i<lines.length-1;i++){
    if(lines[i].trim()===`- generic: ${label}`){
      const m=lines[i+1].trim().match(/^- (?:strong|code|generic): (.+)$/);
      if(m)return m[1];
    }
  }
  return null;
}
function check(snapshot,item){
  for(const key of ['source_id','md5','approved_source_id','approved_md5','speaker_slug','destination'])
    requireValue(typeof item[key]==='string'&&item[key].length>0,`Missing ${key}`);
  requireValue(item.approval==='approved','Recording not approved');
  requireValue(item.source_id===item.approved_source_id&&item.md5===item.approved_md5,'Approval does not cover these bytes');
  requireValue(snapshot.includes('heading "Validate and Review Destination"'),'Preflight not complete');
  requireValue(field(snapshot,'Drive file ID')===item.source_id,'Wrong source ID');
  requireValue(field(snapshot,'Checksum')===item.md5,'Source changed');
  requireValue(field(snapshot,'GCS status')==='Available','Storage destination is not empty');
  requireValue(field(snapshot,'Story audio record')==='Available','Audio record is not empty');
  requireValue(field(snapshot,'Mode')==='Production','Not production mode');
  requireValue(snapshot.includes('- strong: All preflight checks passed'),'Preflight failed');
  requireValue(field(snapshot,'GCS object path')===item.destination,'Wrong destination');
  requireValue(item.destination.includes(`/speaker_audios/${item.speaker_slug}/stories/`),'Wrong speaker');
  return true;
}
function receipt(snapshot,item){
  requireValue(snapshot.includes('The file was published successfully')&&snapshot.includes('Anonymous request returned the expected content type.'),'Publication not verified; reconcile history before retry');
  const request=snapshot.match(/text: Request ID\n\s+- code: ([^\n]+)/)?.[1];
  const record=snapshot.match(/Record (\d+) saved/)?.[1];
  const seconds=Number(snapshot.match(/\(([\d.]+) seconds\)/)?.[1]);
  requireValue(request&&record&&seconds>0,'Incomplete publication receipt');
  const urls=[...snapshot.matchAll(/https:\/\/[^\s]+/g)].map(x=>x[0]);
  const url=urls.find(u=>{try{return decodeURIComponent(new URL(u).pathname).endsWith('/'+item.destination);}catch{return false;}});
  requireValue(url,'Destination URL missing');
  return {story_id:item.story_id,speaker_id:item.speaker_id,source_id:item.source_id,md5:item.md5,destination:item.destination,request_id:request,story_audio_id:record,duration_seconds:seconds,public_url:url,preflight_destination_empty:true,server_public_url_verified:true,verified_at:new Date().toISOString()};
}
function makePublisher(tab){
  let active=null,submitted=false;
  return {
    check,
    async publish(item){
      requireValue(!active,'Pending publication must be reconciled');
      const snapshot=await tab.playwright.domSnapshot();check(snapshot,item);
      await tab.playwright.getByRole('button',{name:'Continue to Confirm',exact:true}).click();
      const confirm=await tab.playwright.domSnapshot();
      requireValue(field(confirm,'Operation')==='PUBLISH'&&field(confirm,'Destination')===item.destination&&confirm.includes('Production mode'),'Confirmation mismatch');
      active={...item};submitted=true; // caller must persist pending state before invoking publish
      await tab.playwright.getByRole('button',{name:'Publish File',exact:true}).click();
    },
    async settle(item){
      requireValue(submitted&&active&&active.source_id===item.source_id&&active.destination===item.destination,'No matching pending publication');
      await tab.playwright.getByRole('button',{name:'Publish Another File',exact:true}).waitFor({state:'visible',timeoutMs:20000});
      const result=receipt(await tab.playwright.domSnapshot(),active);active=null;submitted=false;return result;
    }
  };
}
if(typeof module!=='undefined')module.exports={check,receipt,makePublisher};
