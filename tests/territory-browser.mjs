import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8771';
const installed=path.join(process.env.USERPROFILE||'','AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(existsSync(installed)?installed:undefined)});
const page=await browser.newPage({viewport:{width:1440,height:1450}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
mkdirSync('output',{recursive:true});
try{
  let s=await (await page.request.get(base+'/api/state')).json();
  assert(s.match.finished&&s.match.result.score,'Use the real finished game from tests/integration.py');
  const score=s.match.result.score,map=s.match.territory;
  assert(!map.estimated);assert.deepEqual(map.points,score.territory);
  const dead=new Set(score.dead.map(p=>p.slice(0,2).join(',')));
  for(const color of ['B','W'])assert.equal(s.match.stones.filter(([x,y,c])=>c===color&&!dead.has(`${x},${y}`)).length+map.points.filter(p=>p[2]===color).length+(color==='W'?6.5:0),score[color==='B'?'black':'white']);
  await page.request.post(base+'/api/settings',{data:{language:'zh-CN'}});
  await page.goto(base);await page.locator('.resume-btn').click();
  await page.locator('#go-board[data-territory="final"]').waitFor();
  assert((await page.locator('.territory-tools').innerText()).includes('终局地盘'));
  await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:'output/final-territory.png',fullPage:true,animations:'disabled'});
  await page.locator('[data-action="territory"]').click();await page.locator('#go-board[data-territory="hidden"]').waitFor();
  await page.reload();await page.locator('.resume-btn').click();await page.locator('#go-board[data-territory="final"]').waitFor();
  assert.deepEqual(errors,[]);
  writeFileSync('test-results/territory-browser.json',JSON.stringify({ok:true,actualCompletedGame:true,score:score.black+' / '+score.white,dead:score.dead.length,markedEmptyPoints:map.points.length,restoredFinalBoard:true},null,2));
  console.log('PASS: real completed-game territory agrees with Chinese area totals, dead-stone marks, toggle and restore.');
}finally{await browser.close();}
