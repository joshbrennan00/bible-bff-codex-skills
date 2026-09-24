const assert=require('node:assert/strict');
const {check,receipt,makePublisher}=require('../.agents/skills/uploading-speaker-stories-into-vercel/scripts/browser_publish.cjs');
const item={approval:'approved',source_id:'demo-file',approved_source_id:'demo-file',md5:'demo-hash',approved_md5:'demo-hash',speaker_slug:'demo',destination:'demo-prefix/speaker_audios/demo/stories/old-testament/demo/narration.mp3'};
const snap=`- heading "Validate and Review Destination" [level=2]
- generic: Drive file ID
- strong: demo-file
- generic: Checksum
- strong: demo-hash
- generic: GCS status
- strong: Available
- generic: Story audio record
- strong: Available
- generic: Mode
- strong: Production
- strong: All preflight checks passed
- generic: GCS object path
- strong: ${item.destination}`;
assert(check(snap,item));
for(const bad of [snap.replace('GCS status\n- strong: Available','GCS status\n- strong: Exists'),snap.replace('Story audio record\n- strong: Available','Story audio record\n- strong: Exists'),snap.replace('demo-hash','changed'),snap.replace('Production','Dry Run'),'Loading'])assert.throws(()=>check(bad,item));
assert.throws(()=>check(snap,{...item,approval:'pending'}));
assert.throws(()=>check(snap,{...item,approved_source_id:'different'}));
(async()=>{
 let clicks=0;const tab={playwright:{domSnapshot:async()=>snap.replace('GCS status\n- strong: Available','GCS status\n- strong: Exists'),getByRole:()=>({click:async()=>{clicks++}})}};
 await assert.rejects(makePublisher(tab).publish(item));assert.equal(clicks,0);
 console.log('Publication guards passed, including zero clicks for existing destination');
})().catch(e=>{console.error(e);process.exitCode=1});

const success=`The file was published successfully
Anonymous request returned the expected content type.
- text: Request ID
  - code: demo-request
Record 1234567890123456789 saved
(12.5 seconds)
- code: https://storage.example.invalid/${item.destination}`;
assert.equal(receipt(success,item).story_audio_id,'1234567890123456789');
assert.throws(()=>receipt(success.replace('Anonymous request returned the expected content type.','Pending'),item));
assert.throws(()=>receipt(success.replace(item.destination,'different'),item));
