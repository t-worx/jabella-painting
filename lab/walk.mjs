// Walk the page at fixed scroll positions in real Chrome and screenshot each.
import { chromium } from 'playwright-core';
import fs from 'node:fs'; import path from 'node:path';
const argv = process.argv.slice(2);
const arg = (n, d) => { const i = argv.indexOf(n); return i > -1 ? argv[i + 1] : d; };
const url = arg('--url', 'http://localhost:4510/');
const out = path.resolve(arg('--out', 'lab/walk'));
const W = +arg('--width', 1440), H = +arg('--height', 900);
const reduced = argv.includes('--reduced-motion');
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, reducedMotion: reduced ? 'reduce' : 'no-preference', isMobile: W < 700, hasTouch: W < 700 });
const page = await ctx.newPage();
const errors = []; page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(url, { waitUntil: 'load' });
await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
await page.waitForFunction(() => document.querySelector('.hero-video')?.classList.contains('is-ready') || document.querySelector('.static-hero'), null, { timeout: 15000 }).catch(() => {});
const total = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
const heroEnd = await page.evaluate(() => document.querySelector('.hero-scroll').offsetHeight - innerHeight);
const ys = [0, heroEnd * 0.2, heroEnd * 0.45, heroEnd * 0.7, heroEnd * 0.9, heroEnd + 10];
for (let y = heroEnd + H * 0.9; y < total; y += H * 0.9) ys.push(y);
ys.push(total);
let i = 0; const report = [];
for (const y of ys) {
  await page.evaluate(y => window.scrollTo(0, y), y);
  await page.waitForTimeout(500);
  const info = await page.evaluate(() => { const v = document.querySelector('.hero-video'); return { y: scrollY, t: v ? +v.currentTime.toFixed(2) : null, op: document.querySelector('.hero-copy')?.style.opacity }; });
  const f = path.join(out, String(i++).padStart(2, '0') + '.png');
  await page.screenshot({ path: f });
  report.push(info);
}
fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify({ report, errors }, null, 2));
console.log(JSON.stringify({ frames: i, errors, report }));
await browser.close();
