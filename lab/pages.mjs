import { chromium } from 'playwright-core';
import fs from 'node:fs';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const base = process.argv[2] || 'http://localhost:4510';
const paths = ['/', '/residential/interior/', '/residential/exterior/', '/residential/garage/', '/residential/cabinets/', '/residential/popcorn/'];
fs.mkdirSync('lab/pages', { recursive: true });
const out = {};
for (const [name, vp] of [['desktop', { width: 1440, height: 900 }], ['tablet', { width: 1024, height: 768 }], ['phone', { width: 390, height: 844 }]]) {
  const ctx = await browser.newContext({ viewport: vp, isMobile: vp.width < 700, hasTouch: vp.width < 700 });
  for (const p of paths) {
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    const resp = await page.goto(base + p, { waitUntil: 'load' });
    await page.addStyleTag({ content: 'html{scroll-behavior:auto!important} [data-reveal],[data-stagger]>*{opacity:1!important;transform:none!important}' });
    await page.waitForTimeout(400);
    const broken = await page.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')));
    const r = { status: resp.status(), errs, broken, title: await page.title() };
    if (name === 'desktop') {
      r.h1 = await page.locator('h1').first().innerText();
      await page.hover('.nav-sub-toggle'); await page.waitForTimeout(300);
      r.dropdownHover = await page.locator('.nav-sub').isVisible();
      r.dropdownLinks = await page.locator('.nav-sub a').count();
      await page.mouse.move(10, 400); await page.waitForTimeout(300);
      r.dropdownClosed = !(await page.locator('.nav-sub').isVisible());
      await page.click('.nav-sub-toggle'); await page.waitForTimeout(250);
      r.dropdownClick = await page.locator('.nav-sub-toggle').getAttribute('aria-expanded');
      await page.keyboard.press('Escape'); await page.waitForTimeout(250);
      r.dropdownEsc = await page.locator('.nav-sub-toggle').getAttribute('aria-expanded');
      r.current = await page.locator('.desktop-nav a[aria-current="page"]').count();
      if (p !== '/') await page.screenshot({ path: `lab/pages/${p.split('/')[2]}-desktop.png`, fullPage: true });
      if (await page.locator('#compare').count()) {
        const b = await page.locator('#compare').boundingBox();
        await page.locator('#compare').scrollIntoViewIfNeeded(); const bb = await page.locator('#compare').boundingBox();
        await page.mouse.move(bb.x + bb.width * 0.5, bb.y + bb.height * 0.5); await page.mouse.down(); await page.mouse.move(bb.x + bb.width * 0.25, bb.y + bb.height * 0.5, { steps: 6 }); await page.mouse.up();
        r.comparePos = await page.evaluate(() => document.getElementById('compare').style.getPropertyValue('--pos'));
      }
    }
    if (name === 'tablet' && p === '/') {
      r.headerOverflow = await page.evaluate(() => { const h = document.querySelector('.site-header'); return h.scrollWidth > h.clientWidth; });
      await page.screenshot({ path: 'lab/pages/header-tablet.png', clip: { x: 0, y: 0, width: 1024, height: 90 } });
    }
    if (name === 'phone') {
      await page.locator('.menu-toggle').tap(); await page.waitForTimeout(300);
      r.mobileGroupLinks = await page.locator('#mobile-nav .mobile-group a').count();
      r.mobileOpen = await page.locator('#mobile-nav').isVisible();
      if (p === '/residential/interior/') await page.screenshot({ path: 'lab/pages/mobile-menu.png' });
      await page.locator('.menu-toggle').tap();
      if (p !== '/') await page.screenshot({ path: `lab/pages/${p.split('/')[2]}-phone.png`, fullPage: true });
    }
    out[`${name} ${p}`] = r;
    await page.close();
  }
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify(out, null, 1));
