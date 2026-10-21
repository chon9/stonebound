import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const exe=path.join(process.env.USERPROFILE,'AppData/Local/ms-playwright/chromium-1193/chrome-win/chrome.exe');
const browser=await chromium.launch({headless:true,executablePath:exe});
try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  await page.goto('https://3k.chon9.com/',{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForTimeout(1800);
  await page.screenshot({path:'output/reference-ui.png',fullPage:true});
  console.log(await page.locator('body').innerText());
  console.log(JSON.stringify(await page.evaluate(()=>({title:document.title,colors:[...document.querySelectorAll('body,header,main,nav,button')].slice(0,20).map(el=>({tag:el.tagName,class:el.className,bg:getComputedStyle(el).backgroundColor,font:getComputedStyle(el).fontFamily})),images:[...document.images].slice(0,20).map(i=>({src:i.src,alt:i.alt}))})),null,2));
}finally{await browser.close();}
