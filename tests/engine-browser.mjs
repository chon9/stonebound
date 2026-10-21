import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8773';
assert(['127.0.0.1','localhost'].includes(new URL(base).hostname));
const installed=path.join(process.env.USERPROFILE||'','AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(existsSync(installed)?installed:undefined)});
const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
mkdirSync('output',{recursive:true});mkdirSync('test-results',{recursive:true});
const state=()=>page.request.get(base+'/api/state').then(r=>r.json());
async function post(route,data={}){const r=await page.request.post(base+'/api/'+route,{data});assert.equal(r.status(),200,await r.text());return r.json();}
async function wait(check,timeout=120000){const end=Date.now()+timeout;while(Date.now()<end){const s=await state();if(check(s))return s;await new Promise(r=>setTimeout(r,250));}throw Error('Timed out waiting for engine/game state');}
async function clickPoint(x,y){const c=page.locator('#go-board'),box=await c.boundingBox();await c.click({position:{x:(76+x*848/18)/1000*box.width,y:(76+(18-y)*848/18)/1000*box.height}});}
async function settle(){return wait(s=>s.match&&!s.match.thinking&&!s.match.error);}
try{
  let s=await wait(s=>s.engine.status==='ready',300000);
  if(s.match&&!s.match.finished){await settle();await post('match/abandon');}
  if(s.engine.backend!=='cpu'){await post('settings',{ai_backend:'cpu'});await wait(s=>!s.engine.switching&&s.engine.backend==='cpu');}
  await post('settings',{language:'en'});await post('match/start',{opponent:'haru',size:19});
  await page.goto(base);await page.locator('.resume-btn').click();await page.locator('#go-board').waitFor();
  // Hold the request itself: the submitted stone must paint before any server reply.
  let release,requests=0;
  const held=new Promise(resolve=>release=resolve);
  await page.route('**/api/match/play',async route=>{requests++;await held;await route.continue();});
  const brightness=()=>page.locator('#go-board').evaluate(c=>{const d=c.getContext('2d').getImageData(Math.round(76+3*848/18)+5,Math.round(76+15*848/18)+5,1,1).data;return d[0]+d[1]+d[2];});
  const empty=await brightness();const clickStart=Date.now();await clickPoint(3,3);
  await page.waitForFunction(()=>document.querySelector('#go-board')?.dataset.pending==='3,3');
  const paintMs=Date.now()-clickStart;assert(paintMs<500,`Pending stone took ${paintMs} ms`);
  assert((await brightness())<empty-100,'The pending stone must actually be painted');
  assert.equal((await state()).match.moveNumber,0,'The request is still held');
  await clickPoint(4,4);assert.equal(requests,1,'Duplicate placement must be blocked while submitting');
  const responsePromise=page.waitForResponse(r=>r.url()===base+'/api/match/play');
  const submitted=Date.now();release();const response=await responsePromise;const ackMs=Date.now()-submitted;
  assert.equal(response.status(),200);assert(ackMs<500,`Placement acknowledgement took ${ackMs} ms`);
  s=await settle();assert.equal(s.match.moveNumber,2);assert(s.match.review,'Coaching must still complete');
  await page.unroute('**/api/match/play');
  console.log(JSON.stringify({pending_paint_ms:paintMs,placement_ack_ms:ackMs,actual_cpu_moves:s.match.moves}));
  // Rejected moves remove the tentative stone and leave the real position intact.
  await wait(s=>s.match.moveNumber===2);await page.waitForFunction(()=>document.querySelector('.move-indicator')?.textContent.includes('3'));
  await page.route('**/api/match/play',route=>route.fulfill({status:400,contentType:'application/json',body:JSON.stringify({error:'Rejected test move'})}));
  await clickPoint(4,4);await page.locator('#toast.show').filter({hasText:'Rejected test move'}).waitFor();
  await page.waitForFunction(()=>document.querySelector('#go-board')?.dataset.pending==='');
  assert.equal((await state()).match.moveNumber,2);await page.unroute('**/api/match/play');
  const before=await state();
  await page.locator('.bottom-dock [data-action="settings"]').click();await page.locator('[data-ai-backend="gpu"]').click();
  s=await wait(s=>!s.engine.switching,300000);assert.equal(s.engine.backend,'gpu',s.engine.switchError);
  assert.equal(s.profile.ai_backend,'gpu');assert.deepEqual(s.match.moves,before.match.moves);assert.equal(s.match.id,before.match.id);assert.equal(s.profile.coins,before.profile.coins);
  await page.waitForFunction(()=>document.querySelector('[data-active-backend]')?.textContent.includes('GPU'));
  await page.waitForFunction(()=>!document.querySelector('#toast.show'));
  await page.screenshot({path:'output/engine-settings.png',fullPage:true,animations:'disabled'});
  await page.locator('.modal-close').click();await clickPoint(4,4);s=await settle();assert.equal(s.match.moveNumber,4);assert(s.match.review);
  const gpuMoves=s.match.moves;
  await page.locator('.bottom-dock [data-action="settings"]').click();await page.locator('[data-ai-backend="cpu"]').click();
  s=await wait(s=>!s.engine.switching);assert.equal(s.engine.backend,'cpu',s.engine.switchError);assert.deepEqual(s.match.moves,gpuMoves);
  await page.reload();await page.locator('.bottom-dock [data-action="settings"]').click();
  assert((await page.locator('[data-active-backend]').innerText()).includes('CPU'));
  await page.locator('[data-language="zh-CN"]').click();await page.locator('html[lang="zh-CN"]').waitFor();
  assert((await page.locator('.ai-settings').innerText()).includes('AI运算设备'));
  await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.locator('[data-ai-backend="gpu"]').scrollIntoViewIfNeeded();assert(await page.locator('[data-ai-backend="gpu"]').isVisible());
  await page.keyboard.press('Escape');await post('match/abandon');assert.deepEqual(errors,[]);
  writeFileSync('test-results/engine-browser.json',JSON.stringify({ok:true,pending_paint_ms:paintMs,placement_ack_ms:ackMs,board:19,real_cpu_and_gpu_turns:true,switch_preserves_board:true,choice_persists:true,rejected_move_rollback:true,duplicate_click_guard:true,bilingual_mobile_settings:true},null,2));
  console.log('PASS: immediate 19×19 placement, rollback/duplicate guards, actual CPU/GPU replies, switching without losing the board and persistent bilingual settings.');
}catch(error){await page.screenshot({path:'test-results/engine-failure.png',fullPage:true,animations:'disabled'}).catch(()=>{});throw error;}finally{await browser.close();}
