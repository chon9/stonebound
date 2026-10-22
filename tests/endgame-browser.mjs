import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8776';
assert(['127.0.0.1','localhost'].includes(new URL(base).hostname));
const installed=path.join(process.env.USERPROFILE||'','AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(existsSync(installed)?installed:undefined)});
const page=await browser.newPage({viewport:{width:1440,height:1150}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
mkdirSync('output',{recursive:true});mkdirSync('test-results',{recursive:true});
const state=()=>page.request.get(base+'/api/state').then(r=>r.json());
async function post(route,data={}){const r=await page.request.post(base+'/api/'+route,{data});assert.equal(r.status(),200,await r.text());return r.json();}
async function wait(check,timeout=120000){const end=Date.now()+timeout;while(Date.now()<end){const s=await state();if(s.match?.error)throw Error(s.match.error);if(check(s))return s;await new Promise(r=>setTimeout(r,250));}throw Error('Engine/game state timed out');}
try{
  let s=await wait(s=>s.engine.status==='ready',300000);
  assert(s.match&&!s.match.finished&&s.match.next==='B','Serve a settled position immediately before the player pass.');
  const before=s.match.moveNumber;
  await post('settings',{language:'en'});await page.goto(base);await page.locator('.resume-btn').click();
  assert((await page.locator('[data-action="pass"]').getAttribute('title')).includes('Choose Resign'));
  await page.locator('[data-action="pass"]').click();s=await wait(s=>s.match.finished);
  assert.equal(s.match.moveNumber,before+2);
  assert.deepEqual(s.match.moves.slice(-2),[['B','pass'],['W','pass']]);
  assert(s.match.result.score);assert(s.match.territory&&!s.match.territory.estimated);
  const result=s.match.result.label;
  await page.locator('.result-panel').waitFor();await page.screenshot({path:'output/friendly-pass-result.png',fullPage:true,animations:'disabled'});
  await post('match/start',{opponent:'haru',size:19});await page.reload();await page.locator('.resume-btn').click();
  await page.locator('[data-action="pass"]').click();s=await wait(s=>!s.match.thinking&&s.match.moveNumber===2);
  assert(!s.match.finished);assert.notEqual(s.match.moves[1][1],'pass');
  await page.locator('.pass-explanation').waitFor();assert((await page.locator('.pass-explanation').innerText()).includes('it does not concede'));
  await page.locator('[data-action="language"]').click();await page.locator('html[lang="zh-CN"]').waitFor();
  assert((await page.locator('.pass-explanation').innerText()).includes('停一手并非认输'));
  await page.locator('[data-action="resign-dialog"]').click();await page.locator('[data-action="resign"]').click();
  s=await wait(s=>s.match.finished);assert.equal(s.match.result.label,'W+R');
  assert.deepEqual(errors,[]);
  writeFileSync('test-results/endgame-browser.json',JSON.stringify({ok:true,settled_position_ended_in_two_passes:true,initial_move_count:before,final_move_count:before+2,result,opening_pass_continues:true,resignation_concedes:true,bilingual_explanation:true,final_territory:true},null,2));
  console.log('PASS: settled game ends in two passes, early pass continues, bilingual pass explanation, resignation and final territory.');
}catch(error){await page.screenshot({path:'test-results/endgame-failure.png',fullPage:true,animations:'disabled'}).catch(()=>{});throw error;}finally{await browser.close();}
