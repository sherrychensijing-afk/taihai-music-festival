const puppeteer = require('puppeteer');
const path = require('path');

const FILE = 'file://' + path.resolve(__dirname, 'taihai-music-festival-prototype.html');
const OUT = path.resolve(__dirname, 'img');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 430, height: 1100, deviceScaleFactor: 2 });
  await page.goto(FILE, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 600));

  // 1) 主页面全景
  await page.screenshot({ path: path.join(OUT, '01-main.png'), fullPage: true });
  console.log('saved 01-main.png');

  // 2) 任务浮层展开
  await page.evaluate(() => openSheet('taskSheet'));
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(OUT, '02-task-sheet.png') });
  console.log('saved 02-task-sheet.png');

  // 3) 充能浮层展开
  await page.evaluate(() => { closeSheet(); openBet(0); });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(OUT, '03-bet-sheet.png') });
  console.log('saved 03-bet-sheet.png');

  // 4) 艺人卡展开节点奖励
  await page.evaluate(() => {
    closeSheet();
    const c = document.querySelector('.acard');
    c.scrollIntoView();
  });
  await new Promise(r => setTimeout(r, 400));
  await page.evaluate(() => document.querySelector('.acard').click());
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: path.join(OUT, '04-artist-expand.png') });
  console.log('saved 04-artist-expand.png');

  await browser.close();
  console.log('ALL DONE');
})().catch(e => { console.error(e); process.exit(1); });
