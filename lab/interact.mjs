// Exercise the interactive pieces in real Chrome: compare slider, FAQ, form, mobile menu.
import { chromium } from 'playwright-core';
import fs from 'node:fs'; import path from 'node:path';
const out = path.resolve('lab/interact'); fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const exe = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser = await chromium.launch({ executablePath: exe, headless: true });
const res = {};
// desktop
let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
let page = await ctx.newPage();
await page.goto('http://localhost:4510/', { waitUntil: 'load' });
await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
// compare slider: drag knob from centre to 20%
const frame = page.locator('#compare');
await frame.scrollIntoViewIfNeeded(); await page.evaluate(() => scrollBy(0, -120)); await page.waitForTimeout(600);
const b = await frame.boundingBox();
await page.mouse.move(b.x + b.width * 0.5, b.y + b.height * 0.5); await page.mouse.down();
await page.mouse.move(b.x + b.width * 0.2, b.y + b.height * 0.5, { steps: 8 }); await page.mouse.up();
res.comparePos = await page.evaluate(() => document.getElementById('compare').style.getPropertyValue('--pos'));
await page.screenshot({ path: path.join(out, 'compare.png') });
// keyboard on the range
await page.locator('.compare__range').focus(); await page.keyboard.press('End');
res.compareEnd = await page.evaluate(() => document.getElementById('compare').style.getPropertyValue('--pos'));
// FAQ
await page.locator('#faq summary').nth(1).click(); await page.locator('#faq').scrollIntoViewIfNeeded(); await page.waitForTimeout(400);
res.faqOpen = await page.locator('#faq details[open]').count();
await page.screenshot({ path: path.join(out, 'faq.png') });
// form: submit empty, then fill
await page.locator('#estimate-form').scrollIntoViewIfNeeded(); await page.waitForTimeout(400);
await page.locator('#estimate-form button[type=submit]').click();
res.invalidCount = await page.locator('#estimate-form .is-invalid').count();
await page.fill('input[name=name]', 'Test Homeowner'); await page.fill('input[name=email]', 'test@example.com');
await page.fill('input[name=address]', '33432'); await page.selectOption('select[name=service]', { label: 'Exterior painting' });
await page.fill('textarea[name=details]', 'Two-story stucco exterior, some fascia repair.');
await page.locator('#estimate-form button[type=submit]').click(); await page.waitForTimeout(300);
res.done = await page.locator('.form__done').isVisible();
await page.screenshot({ path: path.join(out, 'form.png') });
// tab order: first 8 focus stops
await page.evaluate(() => scrollTo(0, 0)); const stops = [];
for (let i = 0; i < 8; i++) { await page.keyboard.press('Tab'); stops.push(await page.evaluate(() => { const a = document.activeElement; return a.tagName + (a.textContent ? ':' + a.textContent.trim().slice(0, 24) : ''); })); }
res.tabStops = stops;
await ctx.close();
// mobile menu
ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
page = await ctx.newPage(); await page.goto('http://localhost:4510/', { waitUntil: 'load' }); await page.waitForTimeout(500);
await page.locator('.menu-toggle').tap(); await page.waitForTimeout(300);
res.mobileNavOpen = await page.locator('#mobile-nav').isVisible();
await page.screenshot({ path: path.join(out, 'mobile-menu.png') });
await page.locator('#mobile-nav a[href="#services"]').tap(); await page.waitForTimeout(800);
res.mobileNavClosedAfterTap = !(await page.locator('#mobile-nav').isVisible());
res.mobileScrolledTo = await page.evaluate(() => Math.round(scrollY));
await browser.close();
console.log(JSON.stringify(res, null, 1));
