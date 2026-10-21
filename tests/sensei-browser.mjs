import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8770';
assert(['127.0.0.1','localhost'].includes(new URL(base).hostname));
const installed=path.join(process.env.USERPROFILE||'','AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(existsSync(installed)?installed:undefined)});
const page=await browser.newPage({viewport:{width:1440,height:1150}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
mkdirSync('output',{recursive:true});mkdirSync('test-results',{recursive:true});
const state=()=>page.request.get(base+'/api/state').then(r=>r.json());
async function post(url,data={}){const r=await page.request.post(base+'/api/'+url,{data});assert.equal(r.status(),200,await r.text());return r.json();}
async function settle(){for(let i=0;i<200;i++){const s=await state();if(!s.match.thinking){assert(!s.match.error,s.match.error);return s;}await new Promise(r=>setTimeout(r,300));}throw Error('Engine timeout');}
try{
  await post('settings',{language:'zh-CN'});await page.goto(base);await page.locator('.spirit-invitation').click();
  await page.locator('.spirit-comic').waitFor();assert.equal(await page.locator('.spirit-comic .comic-panel').count(),3);
  assert((await page.locator('.spirit-comic').innerText()).includes('吾名砚归'));
  await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:'output/spirit-manga.png',fullPage:true,animations:'disabled'});
  await page.locator('[data-spirit-done]').click();
  let s=await state();if(s.match&&!s.match.finished)await post('match/abandon');
  await post('match/start',{opponent:'haru',size:9});
  // A strong empty-board hint is genuinely produced by KataGo.
  s=await post('match/hint');assert.equal(s.match.sensei.preview.points.length,81);assert(s.match.sensei.visits>0);
  const opening=s.match.hint.gtp;
  // Passing on an empty board is a reproducible loss compared with that opening.
  await post('match/pass');s=await settle();assert(s.match.review);assert.equal(s.match.review.played,'pass');
  assert(['mistake','blunder'].includes(s.match.review.severity),JSON.stringify(s.match.review));
  assert(s.match.review.loss>=3);assert.equal(s.match.review.best,opening);
  await page.reload();await page.locator('.resume-btn').click();
  await page.locator('.sensei-review').waitFor();
  assert((await page.locator('.sensei-review').innerText()).includes('估计目损'));
  await page.locator('.sensei-card [data-action="hint"]').click();
  await page.locator('#go-board[data-territory="estimated"]').waitFor();
  await page.locator('.sensei-advice').waitFor();s=await state();
  assert.equal(s.match.hint.gtp,s.match.sensei.gtp);
  assert(s.match.sensei.preview.points.some(p=>p[2]==='W'),'White should have influence after Black passes');
  await page.screenshot({path:'output/sensei-territory.png',fullPage:true,animations:'disabled'});
  await page.locator('[data-action="territory"]').click();await page.locator('#go-board[data-territory="hidden"]').waitFor();
  await page.locator('[data-action="territory"]').click();await page.locator('#go-board[data-territory="estimated"]').waitFor();
  await page.locator('[data-action="undo"]').click();s=await state();assert.equal(s.match.sensei,null);assert.equal(s.match.review,null);assert.equal(s.match.hint,null);
  await page.locator('#go-board[data-territory="hidden"]').waitFor();
  await page.locator('.sensei-card [data-action="hint"]').click();await page.locator('.sensei-advice').waitFor();s=await state();
  const best=s.match.hint;await post('match/play',{point:best.point});s=await settle();assert.equal(s.match.review.severity,'calm');assert.equal(s.match.review.loss,0);
  await page.reload();await page.locator('.resume-btn').click();
  await page.locator('[data-action="resign-dialog"]').click();await page.locator('[data-action="resign"]').click();
  await page.locator('.result-panel').waitFor();await page.locator('#go-board[data-territory="estimated"]').waitFor();
  s=await state();assert.equal(s.match.result.label,'W+R');assert.equal(s.match.result.score,null);assert.equal(s.match.territory.points.length,81);
  await page.reload();await page.locator('.bottom-dock [data-page="lobby"]').click();
  await page.locator('.bottom-dock [data-page="journal"]').click();
  await page.locator('[data-spirit-chapter="1"]').click();await page.locator('.spirit-reflection').waitFor();
  assert((await page.locator('.spirit-reflection').innerText()).includes('你的外婆也能听见我'));
  await page.locator('.spirit-reflection [data-action="language"]').click();await page.locator('html[lang="en"]').waitFor();assert((await page.locator('.spirit-reflection').innerText()).includes('Your grandmother'));
  await page.keyboard.press('Escape');
  // A completed save still exposes the result board through the adventure screen's match route.
  await post('match/start',{opponent:'haru',size:9});await page.reload();await page.locator('.resume-btn').click();
  await page.setViewportSize({width:390,height:844});await page.locator('.sensei-card').scrollIntoViewIfNeeded();
  assert(await page.locator('.sensei-card').isVisible(),'Sensei must remain accessible on mobile');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:'output/sensei-mobile.png',fullPage:true,animations:'disabled'});
  await post('match/abandon');assert.deepEqual(errors,[]);
  writeFileSync('test-results/sensei-browser.json',JSON.stringify({ok:true,realBlunderReview:true,realBestMove:true,ownershipPreview:true,resignationEstimate:true,story:true,bilingual:true,mobile:true},null,2));
  console.log('PASS: real KataGo blunder review, best move, territory orientation/overlay, undo invalidation, resignation map, bilingual ghost manga/reflections and mobile mentor.');
}catch(error){await page.screenshot({path:'test-results/sensei-failure.png',fullPage:true,animations:'disabled'}).catch(()=>{});throw error;}finally{await browser.close();}
