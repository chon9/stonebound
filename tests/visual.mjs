// Targeted visual QA; preserves the player's original language preference.
import {chromium} from 'playwright';
import {existsSync,mkdirSync} from 'node:fs';
import path from 'node:path';
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8766';
const exe=path.join(process.env.USERPROFILE||'','AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(existsSync(exe)?exe:undefined)});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const remote=[];page.on('request',r=>{if(!r.url().startsWith(base))remote.push(r.url());});
const initial=await page.request.get(`${base}/api/state`).then(r=>r.json());
async function language(value){await page.request.post(`${base}/api/settings`,{data:{language:value}});await page.goto(base);await page.locator('.begin-btn').waitFor();await page.locator(`html[lang="${value}"]`).waitFor();}
async function shot(name){await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:`output/${name}.png`,fullPage:true,animations:'disabled'});}
try{
  mkdirSync('output',{recursive:true});
  await language('en');await shot('stonebound-lobby-en');await shot('stonebound-preview');
  await language('zh-CN');await shot('stonebound-lobby-zh');
  for(const destination of ['city','shop','collection','journal']){await page.locator(`.bottom-dock [data-page="${destination}"]`).click();await shot(`stonebound-${destination}`);}
  await page.setViewportSize({width:390,height:844});await page.locator('.bottom-dock [data-page="lobby"]').click();await shot('stonebound-mobile-zh');
  if(remote.length)throw new Error('Unexpected external requests: '+remote.join(', '));
  console.log('PASS: redesigned city/lobby/shop/collection/journal/mobile screenshots, no external runtime requests.');
}finally{await page.request.post(`${base}/api/settings`,{data:{language:initial.profile.language}});await browser.close();}
