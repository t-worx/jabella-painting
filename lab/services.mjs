import { chromium } from 'playwright-core';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
for (const [name, vp] of [['desktop', { width: 1440, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
  const page = await (await browser.newContext({ viewport: vp })).newPage();
  const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('http://localhost:4510/', { waitUntil: 'load' });
  await page.addStyleTag({ content: 'html{scroll-behavior:auto!important} [data-reveal],[data-stagger]>*{opacity:1!important;transform:none!important}' });
  await page.locator('#services').scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
  await page.locator('#services').screenshot({ path: `lab/services-${name}.png` });
  const broken = await page.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')));
  console.log(name, JSON.stringify({ cards: await page.locator('.card').count(), broken, errs }));
}
await browser.close();
