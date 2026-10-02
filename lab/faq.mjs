import { chromium } from 'playwright-core';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await page.goto('http://localhost:4510/', { waitUntil: 'load' });
await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
await page.locator('#faq').scrollIntoViewIfNeeded(); await page.waitForTimeout(300);
const d = page.locator('#faq details').nth(0); const body = d.locator('.acc__body');
const h = async () => body.evaluate(el => Math.round(el.getBoundingClientRect().height));
await d.locator('summary').click(); await page.waitForTimeout(100); const mid = await h();
await page.waitForTimeout(400); const open = await h(); const isOpen = await d.evaluate(el => el.open);
await page.screenshot({ path: 'lab/faq-open.png', clip: { x: 700, y: 200, width: 640, height: 450 } });
await d.locator('summary').click(); await page.waitForTimeout(100); const midClose = await h(); const closingClass = await d.evaluate(el => el.classList.contains('is-closing'));
await page.waitForTimeout(400); const closed = await d.evaluate(el => el.open);
// second one opens while first is closed; keyboard works too
await page.locator('#faq details').nth(2).locator('summary').focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(450);
const thirdOpen = await page.locator('#faq details').nth(2).evaluate(el => el.open);
console.log(JSON.stringify({ midOpenHeight: mid, finalOpenHeight: open, isOpen, midCloseHeight: midClose, closingClass, closedAfter: !closed, thirdOpenViaKeyboard: thirdOpen, errs }));
await browser.close();
