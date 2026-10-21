import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync} from 'node:fs';
import path from 'node:path';

const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8769';
assert(['localhost','127.0.0.1'].includes(new URL(base).hostname));
const installed=path.join(process.env.USERPROFILE,'AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:existsSync(installed)?installed:undefined});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],remote=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('request',r=>{if(!r.url().startsWith(base))remote.push(r.url());});
const state=()=>page.request.get(base+'/api/state').then(r=>r.json());
const post=(route,data)=>page.request.post(base+'/api/'+route,{data});
const waitState=async fn=>{for(let i=0;i<100;i++){const s=await state();if(fn(s))return s;await new Promise(r=>setTimeout(r,100));}throw new Error('State did not settle.');};
const playing=async id=>page.waitForFunction(id=>{const a=document.querySelector('#bgm-audio');return a?.currentSrc.endsWith('/'+id+'.mp3')&&!a.paused&&a.currentTime>.05&&a.readyState>=2;},id,{timeout:20000});
const selected=async id=>{await page.locator(`[data-music-track="${id}"]`).click();await waitState(s=>s.profile.music_track===id);await playing(id);};
async function shot(name){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:'output/'+name+'.png',animations:'disabled'});}

try{
  mkdirSync('output',{recursive:true});mkdirSync('test-results',{recursive:true});
  await post('settings',{language:'en',music:true,music_volume:.22,music_track:'vaporware',sound:true});
  await page.goto(base);await page.locator('.begin-btn').waitFor();
  assert.equal(await page.locator('#bgm-audio').count(),1);
  assert(await page.locator('#bgm-audio').evaluate(a=>a.paused),'Wait for a real user interaction before playing.');
  await page.evaluate(()=>{window.musicStarts=0;document.querySelector('#bgm-audio').addEventListener('play',()=>window.musicStarts++);});
  await page.locator('[data-action="music"]').click();await waitState(s=>!s.profile.music);
  assert.equal(await page.evaluate(()=>window.musicStarts),0,'A first click on mute must not start a burst of music.');
  await page.locator('[data-action="music"]').click();await playing('vaporware');
  await page.evaluate(()=>window.originalAudio=document.querySelector('#bgm-audio'));

  // Verify actual decoded audio, rather than only checking button state.
  await page.evaluate(async()=>{const c=new AudioContext();await c.resume();const source=c.createMediaElementSource(document.querySelector('#bgm-audio'));const analyser=c.createAnalyser();source.connect(analyser);analyser.connect(c.destination);window.musicMeter={c,analyser};});
  await page.waitForFunction(()=>{const data=new Uint8Array(window.musicMeter.analyser.fftSize);window.musicMeter.analyser.getByteTimeDomainData(data);return data.some(v=>v!==128);});

  // End of a recording advances automatically; state polling must not reset it.
  await page.locator('#bgm-audio').evaluate(a=>a.currentTime=a.duration-.15);
  await playing('another-august');
  await post('settings',{sound:false});await waitState(s=>!s.profile.sound);
  await page.waitForTimeout(2400);await playing('another-august');

  const before=await page.locator('#bgm-audio').evaluate(a=>a.currentTime);
  for(const destination of ['city','shop','collection','journal','learn','lobby']){
    await page.locator(`.bottom-dock [data-page="${destination}"]`).click();
    assert(await page.evaluate(()=>window.originalAudio===document.querySelector('#bgm-audio')));
  }
  assert((await page.locator('#bgm-audio').evaluate(a=>a.currentTime))>=before);
  await page.locator('.bottom-dock [data-action="settings"]').click();
  assert.equal(await page.locator('[data-music-track]').count(),4);
  for(const track of (await state()).music){await selected(track.id);assert((await page.locator('#bgm-audio').evaluate(a=>a.duration))>30);}
  await page.locator('#bgm-audio').evaluate(a=>a.currentTime=a.duration-.15);await playing('vaporware');
  await page.locator('[data-action="music-next"]').click();await playing('another-august');
  await page.locator('[data-action="music-previous"]').click();await playing('vaporware');

  await page.locator('#music-volume').evaluate(el=>{el.value='37';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));});
  await waitState(s=>s.profile.music_volume===.37);
  assert.equal(await page.locator('#bgm-audio').evaluate(a=>a.volume),.37);
  assert.equal(await page.locator('[data-music-percent]').innerText(),'37%');
  assert.equal((await state()).profile.sound,false,'Music controls must not change stone-sound preferences.');
  await page.locator('[data-action="music-settings"]').click();await waitState(s=>!s.profile.music);
  assert(await page.locator('#bgm-audio').evaluate(a=>a.paused));
  await page.locator('[data-action="music-settings"]').click();await playing('vaporware');
  await shot('stonebound-music-en');
  await page.locator('[data-language="zh-CN"]').click();await page.locator('html[lang="zh-CN"]').waitFor();
  assert.equal(await page.locator('[data-music-title]').innerText(),'云间琴声');
  await playing('vaporware');await shot('stonebound-music-zh');

  // A bad local media file should skip without stopping the game or looping errors.
  await page.route('**/assets/music/another-august.mp3',route=>route.fulfill({status:404,body:''}));
  await page.locator('[data-music-track="another-august"]').click();
  await waitState(s=>s.profile.music_track==='another-august');await playing('synthwave-4k');
  await page.unroute('**/assets/music/another-august.mp3');await selected('another-august');
  await page.locator('[data-action="music-settings"]').click();await waitState(s=>!s.profile.music);
  await page.reload();await page.locator('.begin-btn').waitFor();
  assert(await page.locator('#bgm-audio').evaluate(a=>a.paused));
  assert.equal((await state()).profile.music_volume,.37);
  assert.equal((await state()).profile.music_track,'another-august');
  await page.locator('.bottom-dock [data-action="settings"]').click();
  assert.equal(await page.locator('[data-music-title]').innerText(),'又一个八月');
  await page.setViewportSize({width:390,height:844});await shot('stonebound-music-mobile');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.locator('[data-action="music-settings"]').click();await playing('another-august');

  // HTTP byte ranges let the native player seek to the next song reliably.
  const track=(await state()).music[0];
  let response=await page.request.get(base+track.file,{headers:{Range:'bytes=0-31'}});
  assert.equal(response.status(),206);assert.equal((await response.body()).length,32);
  assert.equal(response.headers()['content-range'],`bytes 0-31/${track.bytes}`);
  response=await page.request.get(base+track.file,{headers:{Range:'bytes=-16'}});assert.equal(response.status(),206);assert.equal((await response.body()).length,16);
  response=await page.request.get(base+track.file,{headers:{Range:'bytes=999999999-'}});assert.equal(response.status(),416);
  response=await page.request.get(base+track.file,{headers:{Range:'bytes=10-1'}});assert.equal(response.status(),416);
  response=await page.request.get(base+track.file,{headers:{Range:'bytes=-0'}});assert.equal(response.status(),416);
  assert.deepEqual(errors,[]);assert.deepEqual(remote,[],'Playback must remain entirely local.');
  console.log('PASS: four real decoded CC0 tracks; gesture start; no mute burst; auto advance and wrap; persistent playback across pages; independent SFX/music; volume and track persistence; bilingual/mobile controls; bad-file recovery; byte ranges; no external requests.');
}catch(error){await page.screenshot({path:'test-results/music-failure.png',fullPage:true}).catch(()=>{});throw error;}finally{await browser.close();}
