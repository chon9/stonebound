import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {existsSync,mkdirSync} from 'node:fs';
import path from 'node:path';
const base='http://127.0.0.1:8767';
const exe=path.join(process.env.USERPROFILE,'AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:existsSync(exe)?exe:undefined});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
const state=()=>page.request.get(base+'/api/state').then(r=>r.json());
async function images(){await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.querySelectorAll('[style*="background-image"]')].map(el=>new Promise((resolve,reject)=>{const src=getComputedStyle(el).backgroundImage.match(/url\(["']?(.*?)["']?\)/)?.[1];if(!src)return resolve();const i=new Image;i.onload=resolve;i.onerror=()=>reject(new Error(src));i.src=src;})));});}
async function shot(name){await images();await page.screenshot({path:`output/${name}.png`,fullPage:!(await page.locator('.comic-book').count()),animations:'disabled'});}
try{
  mkdirSync('output',{recursive:true});
  await page.goto(base);await page.locator('.begin-btn').waitFor();
  let s=await state();assert.equal(s.opponents.length,24);assert.equal(s.items.length,48);assert.equal(s.profile.owned.length,10);
  for(let i=1;i<=8;i++){
    const response=await page.request.get(`${base}/assets/comics/chapter-${String(i).padStart(2,'0')}.png`);assert.equal(response.status(),200);
    await page.locator(`[data-chapter="${i}"]`).click();assert.equal(await page.locator('.rival-node').count(),3);
    for(const r of s.opponents.filter(r=>r.chapter===i)){
      await page.locator(`[data-select-rival="${r.id}"]`).click();
      await images();assert((await page.locator('.rank-medallion').innerText()).includes(r.kyu>0?'级':'段'));
    }
  }
  await page.locator('.bottom-dock [data-page="journal"]').click();assert.equal(await page.locator('.chapter-card').count(),8);
  await shot('stonebound-story-archive');
  for(const p of s.story.pages){
    await page.locator(`[data-comic="${p.id}"]`).click();await page.locator('.comic-book').waitFor();
    assert.equal(await page.locator('.comic-panel').count(),3);
    await images();
    if(p.id==='ch01-open'){
      await shot('stonebound-manga-zh');
      await page.locator('.comic-heading [data-action="language"]').click();await page.locator('html[lang="en"]').waitFor();
      assert((await page.locator('.speech-bubble').first().innerText()).includes('Akari'));
      await shot('stonebound-manga-en');
      await page.locator('.comic-heading [data-action="language"]').click();await page.locator('html[lang="zh-CN"]').waitFor();
      await page.locator('[data-comic-move="1"]').click();assert((await page.locator('.comic-heading').innerText()).includes('结章'));
      await page.locator('[data-comic-move="-1"]').click();
    }
    if(p.id==='ch06-close')await shot('stonebound-manga-city');
    if(p.id==='ch08-close')await shot('stonebound-manga-ending');
    await page.locator('[data-comic-done]').click();await page.locator('.comic-book').waitFor({state:'detached'});
  }
  s=await state();assert.equal(s.profile.story_seen.length,16);assert.equal(new Set(s.profile.story_seen).size,16);
  await page.locator('.bottom-dock [data-page="shop"]').click();assert.equal(await page.locator('.treasure-card').count(),48);
  for(const type of ['board','stones']){await page.locator(`[data-filter="${type}"]`).click();assert.equal(await page.locator('.treasure-card').count(),24);}
  await page.locator('[data-filter="story"]').click();assert.equal(await page.locator('.treasure-card').count(),8);await shot('stonebound-keepsakes');
  await page.locator('.bottom-dock [data-page="collection"]').click();
  await page.locator('[data-equip="homecoming"]').click();assert.equal((await state()).profile.equipped.board,'homecoming');
  await page.locator('[data-filter="stones"]').click();await page.locator('[data-equip="champion_seal"]').click();assert.equal((await state()).profile.equipped.stones,'champion_seal');
  await shot('stonebound-collection-expanded');
  await page.setViewportSize({width:390,height:844});
  for(const destination of ['lobby','city','shop','collection','journal']){
    await page.locator(`.bottom-dock [data-page="${destination}"]`).click();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${destination}: mobile overflow`);
  }
  await page.locator('[data-comic="ch08-close"]').click();await shot('stonebound-manga-mobile');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.deepEqual(errors,[]);
  console.log('PASS: all 24 portraits, 48 skins, 16 illustrated manga pages, 48 panels, bilingual reader, saved read state, chapter navigation, eight keepsakes, equipment and mobile layouts.');
}catch(error){await page.screenshot({path:'test-results/campaign-failure.png',fullPage:true});throw error;}finally{await browser.close();}
