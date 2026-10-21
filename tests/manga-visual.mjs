import {chromium} from 'playwright';
import path from 'node:path';
const browser=await chromium.launch({headless:true,executablePath:path.join(process.env.USERPROFILE,'AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe')});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const base=process.env.STONEBOUND_TEST_URL||'http://127.0.0.1:8766';
const comic=process.env.STONEBOUND_COMIC_PAGE||'ch01-open';
if(!['localhost','127.0.0.1'].includes(new URL(base).hostname))throw new Error('Use an isolated local server.');
try{
  await page.goto(base);await page.locator('.begin-btn').waitFor();
  await page.locator('.bottom-dock [data-page="journal"]').click();
  await page.locator(`[data-comic="${comic}"]`).click();
  await page.evaluate(async()=>{await document.fonts.ready;const image=new Image();image.src=document.querySelector('.comic-illustration').style.backgroundImage.match(/url\(["']?(.*?)["']?\)/)[1];await image.decode();});
  await page.screenshot({path:comic==='ch01-open'?'output/stonebound-manga-zh.png':'output/stonebound-manga-ending.png',animations:'disabled'});
  console.log(await page.locator('.comic-illustration').first().evaluate(e=>getComputedStyle(e).backgroundImage));
}finally{await browser.close();}
