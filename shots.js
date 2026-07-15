const puppeteer = require('puppeteer');
const path = require('path');
const FILE = 'file://' + path.resolve(__dirname, 'taihai-music-festival-prototype.html');
const OUT = path.resolve(__dirname, 'img');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 430, height: 1000, deviceScaleFactor: 2 });
  await page.goto(FILE, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 400));

  async function shot(sel, file) {
    const el = await page.$(sel);
    await el.evaluate(e => e.scrollIntoView({ block: 'start' }));
    await new Promise(r => setTimeout(r, 250));
    await el.screenshot({ path: path.join(OUT, file) });
    console.log('shot', file);
  }

  await shot('.kv', 'mod_01_kv.png');
  await shot('.banner', 'mod_02_banner.png');

  const secs = await page.$$('.sec');
  for (let i = 0; i < 3; i++) {
    await secs[i].evaluate(e => e.scrollIntoView({ block: 'start' }));
    await new Promise(r => setTimeout(r, 250));
    const names = ['mod_03_intro.png', 'mod_04_roster.png', 'mod_05_ticket.png'];
    await secs[i].screenshot({ path: path.join(OUT, names[i]) });
    console.log('shot', names[i]);
  }

  await shot('.station-h', 'mod_06_coin.png');
  await shot('#artistList', 'mod_07_artistlist.png');
  await shot('.lottery', 'mod_08_lottery.png');

  // 任务浮层
  await page.evaluate(() => openSheet('taskSheet'));
  await new Promise(r => setTimeout(r, 550));
  await (await page.$('#taskSheet')).screenshot({ path: path.join(OUT, 'mod_09_tasksheet.png') });
  console.log('shot mod_09_tasksheet.png');

  // 充能浮层
  await page.evaluate(() => { closeSheet(); openBet(0); });
  await new Promise(r => setTimeout(r, 550));
  await (await page.$('#betSheet')).screenshot({ path: path.join(OUT, 'mod_10_betsheet.png') });
  console.log('shot mod_10_betsheet.png');

  // 艺人卡展开
  await page.evaluate(() => {
    closeSheet();
    const c = document.querySelector('.acard');
    c.scrollIntoView({ block: 'center' });
    c.click();
  });
  await new Promise(r => setTimeout(r, 550));
  await (await page.$('.acard')).screenshot({ path: path.join(OUT, 'mod_11_expand.png') });
  console.log('shot mod_11_expand.png');

  await browser.close();
  console.log('ALL DONE');
})().catch(e => { console.error(e); process.exit(1); });
