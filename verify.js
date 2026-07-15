const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({args:['--no-sandbox','--disable-setuid-sandbox']});
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type()==='error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: '+e.message));
  await page.goto('file:///Users/chensijing/WorkBuddy/2026-07-15-17-02-13/taihai-music-festival-prototype.html', {waitUntil:'networkidle0'});
  const counts = await page.evaluate(() => ({
    rank: document.querySelectorAll('#artistList .acard').length,
    tasks: document.querySelectorAll('#taskList .task').length,
    grid: document.querySelectorAll('#grid9 .cell').length,
    coin: document.getElementById('coinNow').textContent,
  }));
  console.log('CONSOLE ERRORS:', errors.length ? errors : 'none');
  console.log('RENDER COUNTS:', JSON.stringify(counts));
  await browser.close();
})();
