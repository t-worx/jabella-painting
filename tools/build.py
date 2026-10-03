#!/usr/bin/env python3
"""Render the shared header/footer and the residential child pages.

Run from the build folder after editing anything here:
    python3 tools/build.py

Writes residential/<slug>/index.html for each page in PAGES, and patches the
header and footer inside index.html so the chrome is identical everywhere.
Content was pulled from jabellaservices.com (see CONTENT.md).
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://jabella-painting.vercel.app"
PHONE = "(561) 289-1519"
TEL = "+15612891519"
EMAIL = "johnt@jabellaservices.com"

RESIDENTIAL = [
    ("interior", "Interior Painting"),
    ("exterior", "Exterior Painting"),
    ("garage", "Garage Floors"),
    ("cabinets", "Cabinet Refresh"),
    ("popcorn", "Popcorn Removal"),
]
TOP = [
    ("/#commercial", "Commercial"),
    ("/#remodels", "Remodels"),
    ("/#work", "Our Work"),
    ("/#about", "About"),
    ("/#estimate", "Contact"),
]

CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'


def header():
    sub = "\n".join(f'      <a href="/residential/{s}/">{n}</a>' for s, n in RESIDENTIAL)
    top = "\n".join(f'    <a href="{h}">{n}</a>' for h, n in TOP)
    msub = "\n".join(f'    <a href="/residential/{s}/">{n}</a>' for s, n in RESIDENTIAL)
    mtop = "\n".join(f'  <a href="{h}">{n}</a>' for h, n in TOP)
    return f'''<header class="site-header">
  <a class="brand" href="/" aria-label="Jabella Painting and Carpentry, home">
    <img src="/assets/logo.webp" width="180" height="55" alt="Jabella Painting and Carpentry">
  </a>
  <nav class="desktop-nav" aria-label="Main navigation">
    <div class="has-sub">
      <button type="button" class="nav-sub-toggle" aria-expanded="false" aria-controls="sub-residential">Residential {CHEV}</button>
      <div class="nav-sub" id="sub-residential">
{sub}
      </div>
    </div>
{top}
  </nav>
  <a class="btn btn--primary header-cta" href="/#estimate">Get a free estimate {ARROW}</a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
    <span></span><span></span>
  </button>
</header>
<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>
  <div class="mobile-group">
    <p class="mobile-group__label">Residential</p>
{msub}
  </div>
{mtop}
  <a href="/#estimate" class="btn btn--primary">Get a free estimate</a>
</nav>
'''


def footer():
    svc = "\n".join(f'          <li><a href="/residential/{s}/">{n}</a></li>' for s, n in RESIDENTIAL)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__about">
        <a class="brand brand--footer" href="/" aria-label="Jabella Painting and Carpentry, back to top">
          <img src="/assets/logo-white.webp" width="180" height="55" alt="Jabella Painting and Carpentry">
        </a>
        <p>30+ years of premium residential &amp; commercial painting, carpentry, and remodeling in Palm Beach County, FL.</p>
        <a class="btn btn--light footer__cta" href="/#estimate">Get a free estimate {ARROW}</a>
      </div>

      <nav class="footer__col" aria-labelledby="f-services">
        <h4 id="f-services">Residential</h4>
        <ul>
{svc}
        </ul>
      </nav>

      <nav class="footer__col" aria-labelledby="f-company">
        <h4 id="f-company">Company</h4>
        <ul>
          <li><a href="/#commercial">Commercial</a></li>
          <li><a href="/#remodels">Remodels</a></li>
          <li><a href="/#work">Our work</a></li>
          <li><a href="/#about">About</a></li>
          <li><a href="/#process">Our process</a></li>
          <li><a href="/#faq">FAQ</a></li>
        </ul>
      </nav>

      <nav class="footer__col" aria-labelledby="f-areas">
        <h4 id="f-areas">Service areas</h4>
        <ul>
          <li><a href="/#estimate">Boca Raton</a></li>
          <li><a href="/#estimate">Delray Beach</a></li>
          <li><a href="/#estimate">Highland Beach</a></li>
          <li><a href="/#estimate">Boynton Beach</a></li>
          <li><a href="/#estimate">Manalapan</a></li>
          <li><a href="/#estimate">Palm Beach</a></li>
          <li><a href="/#estimate">Palm Beach County</a></li>
        </ul>
      </nav>

      <div class="footer__col footer__contact">
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>121 E Hart St.<br>Lantana, FL 33462</li>
        </ul>
        <ul class="footer__social" aria-label="Social media">
          <li><a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4v2H7v4h3v6h4v-6h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg></a></li>
          <li><a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3.8" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.1"/></svg></a></li>
          <li><a href="#" aria-label="Google reviews"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.8 6 6.5.7-4.9 4.4 1.4 6.4L12 16.7 6.2 20l1.4-6.4L2.7 9.2l6.5-.7z"/></svg></a></li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom">
      <p>© 2026 Jabella Painting and Carpentry. All rights reserved.</p>
      <ul class="footer__legal">
        <li><a href="#">Privacy policy</a></li>
        <li><a href="#">Terms of service</a></li>
        <li><a href="#top">Back to top {ARROW}</a></li>
      </ul>
    </div>
  </div>
</footer>'''


# ---------------------------------------------------------------- page data
# Block types: intro, features, checks, steps, compare, savings, callout,
# gallery, quotes. Copy adapted from jabellaservices.com.
PAGES = [
    dict(
        slug="interior", nav="Interior Painting",
        title="Interior Painting in Boca Raton and Palm Beach County",
        desc="Interior painting for homes and condos in Boca Raton, Delray Beach and Palm Beach County. Smooth finishes, sharp lines, premium low-VOC paints and full furniture protection. Free estimates.",
        h1="Transform <em>every room</em> in your home.",
        sub="From accent walls to full-home makeovers, our interior painting team delivers flawless results with meticulous attention to detail.",
        hero="/assets/interior.webp", hero_pos="50% 60%",
        hero_alt="A light-filled living room with freshly painted white walls opening to a pool",
        blocks=[
            dict(type="intro", kicker="Professional interior painting", h2="A fresh coat is the fastest way <em>to transform your home.</em>",
                 paras=["Whether you’re updating a single room or refreshing your entire interior, our experienced painters treat your home like their own, protecting furniture, floors and fixtures while delivering smooth, flawless finishes.",
                        "We use premium paints from trusted brands and take the time to properly prep every surface for results that last for years."],
                 img="/assets/r-interior-kitchen.webp", img_alt="A kitchen with freshly painted white cabinets and sage green walls"),
            dict(type="features", kicker="Rooms we paint", h2="Every room, <em>finished right.</em>", items=[
                ("Living rooms and family rooms", "Create a welcoming atmosphere with warm, modern color palettes that reflect your style."),
                ("Kitchens and dining areas", "Durable, washable finishes that stand up to daily life while looking beautiful."),
                ("Bedrooms and nurseries", "Restful colors and low-VOC paints for the rooms where comfort matters most."),
                ("Bathrooms and laundry rooms", "Moisture-resistant coatings that prevent peeling and mildew in humid spaces."),
                ("Hallways, stairs and trim", "Crisp, clean lines on baseboards, crown molding, doors and high-traffic areas."),
            ]),
            dict(type="checks", tint=True, kicker="The Jabella difference", h2="What’s included <em>on every interior.</em>", items=[
                "Free color consultation", "Furniture and floor protection", "Clean, sharp paint lines",
                "Premium low-VOC paints", "Detailed prep and priming", "Final walk-through inspection"]),
            dict(type="gallery", imgs=[("/assets/r-interior-kitchen.webp", "Kitchen with white cabinets and sage walls"), ("/assets/r-interior-living.webp", "Living room with warm neutral walls and a navy accent"), ("/assets/r-interior-great.webp", "Two-story great room with a dark accent wall")]),
            dict(type="quotes", items=[
                ("I needed interior walls painted and some repairs done. John did a great job! Very professional. Everything looks so good. He really makes sure everything looks so good.", "Lynn G.", ""),
                ("Jabella did my interior and exterior painting, restained driveway stamped concrete, and the fence gate fix was an added bonus. House looks amazing, refreshed.", "Melodi L.", "via Angi")]),
        ],
        cta=("Ready to refresh <em>your interior?</em>", "Get a free, no-obligation estimate for your interior painting project."),
    ),
    dict(
        slug="exterior", nav="Exterior Painting",
        title="Exterior Painting in Boca Raton and Palm Beach County",
        desc="Exterior house painting built for Florida sun, salt and storms. Power washing, repairs, priming and premium UV-resistant coatings for stucco, trim, doors and more in Palm Beach County.",
        h1="Curb appeal <em>that lasts.</em>",
        sub="Protect your home from Florida’s sun, rain and humidity with professional exterior painting built to endure.",
        hero="/assets/hero-end.webp", hero_pos="50% 55%",
        hero_alt="A freshly painted white Mediterranean home in Boca Raton at golden hour",
        blocks=[
            dict(type="intro", kicker="More than just a paint job", h2="Your exterior is your first impression, <em>and your first line of defense.</em>",
                 paras=["Florida’s harsh sun, tropical storms and relentless humidity demand more than an ordinary paint job.",
                        "We combine thorough surface preparation with premium weather-resistant coatings to deliver results that look stunning and protect your investment for years to come."],
                 img="/assets/r-exterior-work.webp", img_alt="A Jabella painter on a lift painting the arched facade of a two-story home"),
            dict(type="steps", kicker="Our exterior process", h2="Three things that decide <em>whether a finish lasts.</em>", items=[
                ("Surface preparation", "Power washing, scraping, sanding, caulking and priming. The foundation of a lasting paint job."),
                ("Premium coatings", "UV-resistant, 100% acrylic paints rated for Florida’s intense sun and humidity."),
                ("Weather protection", "Our coatings seal out moisture and resist mildew, chalking and fading for years."),
            ]),
            dict(type="checks", tint=True, kicker="Surfaces we paint", h2="Inside the property line, <em>we paint it.</em>", items=[
                "Stucco and concrete block", "Wood siding and trim", "Front doors and shutters", "Fascia, soffits and eaves",
                "Fencing and railings", "Driveways", "Pool decks", "Patios", "Garage doors"]),
            dict(type="gallery", imgs=[("/assets/r-exterior-1.webp", "Gray one-story home with white trim and palms"), ("/assets/r-exterior-2.webp", "Two-story Mediterranean home in warm tan stucco"), ("/assets/r-exterior-work.webp", "Painter on a lift at an arched entry")]),
            dict(type="quotes", items=[
                ("I had Jabella paint my house exterior and restain my driveway. They showed up when promised, they cleaned up all debris, and finished ahead of schedule!!", "Melodi Leahy", "via Angi"),
                ("We are so very appreciative of John and his painting team as they have consistently gone above and beyond to help us with our complex painting job both during the building process of our house and now post-build. Their attention to detail, professionalism, and willingness to work with us on every aspect has been outstanding.", "Andy Larson", "via Website")]),
        ],
        cta=("Boost your home’s <em>curb appeal.</em>", "Schedule a free exterior painting estimate today."),
    ),
    dict(
        slug="garage", nav="Garage Floors",
        title="Epoxy Garage Floor Coatings in Palm Beach County",
        desc="Durable epoxy and polyaspartic garage floor coatings in solid, flake and metallic finishes. Most installs completed in one day. Serving Boca Raton, Delray Beach and Palm Beach County.",
        h1="Professional <em>epoxy floor</em> coatings.",
        sub="Transform your garage into a clean, polished space with durable, beautiful floor coatings.",
        hero="/assets/garage.webp", hero_pos="50% 60%",
        hero_alt="A garage with a glossy flake epoxy floor and a sports car parked inside",
        blocks=[
            dict(type="intro", kicker="More than just a garage floor", h2="A showroom-quality surface <em>built for daily use.</em>",
                 paras=["A professional epoxy coating transforms a dull, stained concrete floor into a showroom-quality surface. Our industrial-grade coatings are designed to withstand hot tire pickup, chemical spills and years of daily use.",
                        "Whether you want a clean solid color, a decorative flake system or a stunning metallic finish, we deliver results that last."],
                 img="/assets/r-garage-2.webp", img_alt="An organized garage with a light gray epoxy floor and steel cabinets"),
            dict(type="checks", tint=True, kicker="Why choose epoxy?", h2="Tough, clean, <em>and fast to install.</em>", items=[
                "Chemical and stain resistant", "Most installs completed in one day", "Easy to clean and maintain", "Moisture and impact resistant"]),
            dict(type="features", kicker="Coating options", h2="Pick the finish <em>that fits your space.</em>", items=[
                ("Solid color epoxy", "Classic, clean look available in dozens of colors. Great for a sleek showroom finish."),
                ("Decorative flake", "Multi-color chip systems that hide imperfections and add texture for slip resistance."),
                ("Metallic epoxy", "Stunning, one-of-a-kind swirl patterns that create a high-end designer look."),
                ("Polyaspartic coating", "Fast-cure formula that’s ready for foot traffic in hours and vehicles the next day."),
            ]),
            dict(type="gallery", imgs=[("/assets/garage.webp", "Flake epoxy garage floor with a sports car"), ("/assets/r-garage-2.webp", "Light gray epoxy floor with storage cabinets"), ("/assets/r-garage-3.webp", "Glossy white epoxy garage floor")]),
            dict(type="quotes", items=[
                ("Great service! Was refreshing to have someone do quality work in a timely manner! Would highly recommend and plan on using this company again.", "Elizabeth C.", "")]),
        ],
        cta=("Upgrade your <em>garage floor.</em>", "Get a free estimate for a professional epoxy floor coating."),
    ),
    dict(
        slug="cabinets", nav="Cabinet Refresh",
        title="Cabinet Refinishing in Boca Raton and Palm Beach County",
        desc="Kitchen and bathroom cabinet refinishing with a sprayed, factory-smooth finish. The look of new cabinets at a fraction of replacement cost. Free estimates in Palm Beach County.",
        h1="A new kitchen <em>without the renovation.</em>",
        sub="Professional cabinet refinishing that delivers a stunning transformation at a fraction of the cost.",
        hero="/assets/cabinets.webp", hero_pos="50% 50%",
        hero_alt="A kitchen with cabinets refinished in bright white with brass hardware",
        blocks=[
            dict(type="compare", kicker="See the transformation", h2="Same cabinets. <em>New kitchen.</em>",
                 before=("/assets/cab-before.webp", "Kitchen with dated honey-oak cabinets before refinishing"),
                 after=("/assets/cab-after.webp", "The same kitchen with cabinets refinished in white"),
                 caption="Honey oak to bright white. No tear-out.", tall=False),
            dict(type="intro", kicker="Why refinish instead of replace?", h2="Your cabinets are sound. <em>They just need a fresh face.</em>",
                 paras=["Cabinet refinishing gives you the look of a brand-new kitchen or bathroom without the weeks of construction, dust and sky-high costs of a full tear-out.",
                        "Choose from modern whites, warm grays, bold navy or any custom color to match your vision."],
                 img="/assets/r-cabinet-refresh.webp", img_alt="White refinished cabinets with a marble backsplash"),
            dict(type="steps", kicker="Our 4-step process", h2="How we get a <em>factory-smooth finish.</em>", items=[
                ("Deep cleaning and degreasing", "We remove years of built-up grease and grime to ensure perfect adhesion."),
                ("Sanding and prep", "All surfaces are scuff-sanded and any damage is repaired for a smooth foundation."),
                ("Professional priming", "A bonding primer is applied to guarantee the topcoat adheres and lasts."),
                ("Spray application", "We spray multiple coats for a factory-smooth, brush-mark-free finish."),
            ]),
            dict(type="savings", tint=True, kicker="Save thousands", h2="Refinishing costs a fraction <em>of replacement.</em>", rows=[
                ("Full cabinet replacement", "$15,000 to $30,000+", False),
                ("Jabella cabinet refinishing", "$3,500 to $7,000", True)],
                note="Typical ranges for an average kitchen. Your written estimate is the price you pay."),
            dict(type="quotes", items=[
                ("This company is amazing. On time and super fast. Very professional. I would refer them to anyone!!", "Nichole R.", "via Angi")]),
        ],
        cta=("Transform <em>your cabinets.</em>", "Get a free estimate for your cabinet refinishing project."),
    ),
    dict(
        slug="popcorn", nav="Popcorn Removal",
        title="Popcorn Ceiling Removal in Boca Raton and Palm Beach County",
        desc="Popcorn ceiling removal with asbestos testing, full room protection, skim coat and fresh ceiling paint. Smooth, modern ceilings for homes in Palm Beach County.",
        h1="Modernize <em>your ceilings.</em>",
        sub="Remove outdated popcorn texture and enjoy clean, smooth ceilings that brighten every room.",
        hero="/assets/popcorn.webp", hero_pos="50% 35%",
        hero_alt="A smooth, freshly painted ceiling with recessed lights after popcorn texture removal",
        blocks=[
            dict(type="compare", kicker="See the difference", h2="From textured <em>to flawless.</em>",
                 before=("/assets/pop-before.webp", "A popcorn-textured ceiling with recessed lights before removal"),
                 after=("/assets/pop-after.webp", "The same ceiling smooth and freshly painted"),
                 caption="Scraped, skim-coated and painted.", tall=True),
            dict(type="checks", kicker="Why remove popcorn ceilings?", h2="Six reasons <em>homeowners call us.</em>", items=[
                "Outdated look that dates your home", "Collects dust, cobwebs and allergens", "Difficult to paint or repair",
                "Can contain asbestos in pre-1980s homes", "Reduces light reflection in rooms", "Lowers home resale value"]),
            dict(type="callout", tint=True, kicker="Safety first", h2="We test <em>before we touch it.</em>",
                 text="Homes built before 1980 may have asbestos in their popcorn texture. We always test before starting work and follow all EPA guidelines to keep your family safe. Your health and safety are our top priority.",
                 img="/assets/pop-prep.webp", img_alt="A room fully masked in protective plastic sheeting before ceiling work"),
            dict(type="steps", kicker="Our process", h2="Four steps to <em>a smooth ceiling.</em>", items=[
                ("Testing and safety", "We test for asbestos before any work begins. If found, we follow EPA-certified abatement procedures."),
                ("Room preparation", "Furniture is moved, floors and fixtures are covered with protective sheeting."),
                ("Texture removal", "The popcorn texture is carefully scraped away, then surfaces are sanded smooth."),
                ("Skim coat and paint", "A thin skim coat creates a perfectly flat surface, followed by a fresh coat of ceiling paint."),
            ]),
            dict(type="quotes", items=[
                ("I can’t stress enough how much the owner of this company and employees helped me in such a time of need. Professional, reliable, reasonable, efficient. Excellent Work.", "P.D.", "via Angi")]),
        ],
        cta=("Ready for <em>smooth ceilings?</em>", "Get a free estimate for popcorn ceiling removal in your home."),
    ),
]


# ---------------------------------------------------------------- renderers
def head_block(kicker, h2, cls="split"):
    return f'''      <p class="label">{kicker}</p>
      <div class="{cls}">
        <h2>{h2}</h2>
      </div>
'''


def r_intro(b):
    paras = "\n".join(f'          <p class="body">{p}</p>' for p in b["paras"])
    return f'''  <section class="block">
    <div class="wrap grid-2 grid-2--about">
      <div>
        <p class="label">{b["kicker"]}</p>
        <h2>{b["h2"]}</h2>
{paras}
        <a class="textlink" href="/#estimate">Get a free estimate {ARROW}</a>
      </div>
      <div class="intro__media" data-reveal>
        <img src="{b["img"]}" alt="{b["img_alt"]}" loading="lazy">
      </div>
    </div>
  </section>
'''


def r_features(b):
    items = "\n".join(f'        <li><span class="num">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(b["items"]))
    return f'''  <section class="block{' block--tint' if b.get('tint') else ''}">
    <div class="wrap">
{head_block(b["kicker"], b["h2"])}      <ol class="steps steps--auto" data-reveal data-stagger>
{items}
      </ol>
    </div>
  </section>
'''


def r_steps(b):
    items = "\n".join(f'        <li><span class="num">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(b["items"]))
    cols = len(b["items"])
    return f'''  <section class="block{' block--tint' if b.get('tint') else ''}">
    <div class="wrap">
{head_block(b["kicker"], b["h2"])}      <ol class="steps steps--{cols}" data-reveal data-stagger>
{items}
      </ol>
    </div>
  </section>
'''


def r_checks(b):
    items = "\n".join(f'        <li>{t}</li>' for t in b["items"])
    return f'''  <section class="block{' block--tint' if b.get('tint') else ''}">
    <div class="wrap">
{head_block(b["kicker"], b["h2"])}      <ul class="check-list" data-reveal data-stagger>
{items}
      </ul>
    </div>
  </section>
'''


def r_compare(b):
    bimg, balt = b["before"]; aimg, aalt = b["after"]
    return f'''  <section class="block">
    <div class="wrap">
{head_block(b["kicker"], b["h2"])}      <div class="compare{' compare--tall' if b.get('tall') else ''}" data-reveal>
        <div class="compare__frame" id="compare" style="--pos: 50%;">
          <img class="compare__after" src="{aimg}" alt="{aalt}" loading="lazy">
          <img class="compare__before" src="{bimg}" alt="{balt}" loading="lazy">
          <span class="compare__tag compare__tag--before">Before</span>
          <span class="compare__tag compare__tag--after">After</span>
          <div class="compare__line" aria-hidden="true"><span class="compare__knob">‹&nbsp;&nbsp;›</span></div>
          <input class="compare__range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
        </div>
        <div class="compare__foot">
          <p class="compare__caption">{b["caption"]}</p>
          <p class="compare__hint">Drag to compare <span aria-hidden="true">→</span></p>
        </div>
      </div>
    </div>
  </section>
'''


def r_savings(b):
    rows = "\n".join(f'        <li class="savings__row{" is-us" if us else ""}"><span>{l}</span><strong>{p}</strong></li>' for l, p, us in b["rows"])
    return f'''  <section class="block{' block--tint' if b.get('tint') else ''}">
    <div class="wrap">
{head_block(b["kicker"], b["h2"])}      <ul class="savings" data-reveal>
{rows}
      </ul>
      <p class="note">{b["note"]}</p>
    </div>
  </section>
'''


def r_callout(b):
    return f'''  <section class="block{' block--tint' if b.get('tint') else ''}">
    <div class="wrap grid-2 grid-2--about">
      <div class="callout">
        <p class="label">{b["kicker"]}</p>
        <h2>{b["h2"]}</h2>
        <p class="body">{b["text"]}</p>
      </div>
      <div class="intro__media" data-reveal>
        <img src="{b["img"]}" alt="{b["img_alt"]}" loading="lazy">
      </div>
    </div>
  </section>
'''


def r_gallery(b):
    imgs = "\n".join(f'        <figure class="tile"><img src="{s}" alt="{a}" loading="lazy"></figure>' for s, a in b["imgs"])
    return f'''  <section class="block block--flush">
    <div class="wrap">
      <div class="gallery3" data-reveal data-stagger>
{imgs}
      </div>
    </div>
  </section>
'''


def r_quotes(b):
    qs = "\n".join(f'''        <blockquote class="testimonial">
          <p>“{q}”</p>
          <footer><strong>{n}</strong>{(' <span>' + v + '</span>') if v else ''}</footer>
        </blockquote>''' for q, n, v in b["items"])
    return f'''  <section class="block block--surface">
    <div class="wrap">
      <p class="label">What homeowners are saying</p>
      <div class="testimonials" data-reveal data-stagger>
{qs}
      </div>
    </div>
  </section>
'''


RENDER = dict(intro=r_intro, features=r_features, steps=r_steps, checks=r_checks, compare=r_compare,
              savings=r_savings, callout=r_callout, gallery=r_gallery, quotes=r_quotes)


def page(p):
    url = f"{SITE}/residential/{p['slug']}/"
    body = "".join(RENDER[b["type"]](b) for b in p["blocks"])
    cta_h, cta_p = p["cta"]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(p["title"])} | Jabella Painting and Carpentry</title>
<meta name="description" content="{html.escape(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jabella Painting and Carpentry">
<meta property="og:title" content="{html.escape(p["title"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{p["hero"]}">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Inter:wght@400;500;600&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/site.css">
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>

{header()}
<main id="main">
  <section class="page-hero">
    <img src="{p["hero"]}" alt="{p["hero_alt"]}" style="object-position: {p["hero_pos"]}" fetchpriority="high">
    <div class="wrap">
      <p class="crumbs"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#services">Residential</a><span aria-hidden="true">/</span><span aria-current="page">{p["nav"]}</span></p>
      <h1>{p["h1"]}</h1>
      <p class="sub">{p["sub"]}</p>
      <div class="hero-actions">
        <a class="btn btn--light btn--lg" href="/#estimate">Get a free estimate {ARROW}</a>
        <a class="btn btn--ghost btn--lg" href="tel:{TEL}">Call {PHONE}</a>
      </div>
    </div>
  </section>

{body}
  <section class="cta-band">
    <div class="wrap">
      <h2>{cta_h}</h2>
      <p>{cta_p}</p>
      <div class="hero-actions">
        <a class="btn btn--light btn--lg" href="/#estimate">Get your free estimate {ARROW}</a>
        <a class="btn btn--ghost btn--lg" href="tel:{TEL}">Call {PHONE}</a>
      </div>
    </div>
  </section>
</main>

{footer()}

<script src="/site.js" defer></script>
</body>
</html>
'''


def patch_home():
    path = os.path.join(ROOT, "index.html")
    s = open(path).read()
    a = s.index('<header class="site-header">'); b = s.index('<main>')
    s = s[:a] + header() + "\n" + s[b:]
    a = s.rindex('<footer class="site-footer">'); b = s.index('</footer>', a) + len('</footer>')
    s = s[:a] + footer() + s[b:]
    # anchors for menu targets and "learn more" links on the residential cards
    s = s.replace('<aside class="commercial" data-reveal', '<aside class="commercial" id="commercial" data-reveal', 1)
    if 'id="remodels"' not in s:
        s = s.replace('<article class="card">\n          <div class="card__media">\n            <img src="assets/remodel.webp"', '<article class="card" id="remodels">\n          <div class="card__media">\n            <img src="assets/remodel.webp"', 1)
    for slug, name in RESIDENTIAL:
        h3 = {"interior": "Interior painting", "exterior": "Exterior painting", "garage": "Garage floor coatings",
              "cabinets": "Cabinet refresh", "popcorn": "Popcorn ceiling removal"}[slug]
        pat = re.compile(r'(<h3>' + re.escape(h3) + r'</h3>\s*<p>.*?</p>)(?!\s*<a class="card__more")', re.S)
        s = pat.sub(lambda m: m.group(1) + f'\n          <a class="card__more" href="/residential/{slug}/">Learn more {ARROW}</a>', s, count=1)
    if 'id="top"' not in s:
        s = s.replace("<body>", '<body id="top">', 1)
    open(path, "w").write(s)


def main():
    for p in PAGES:
        d = os.path.join(ROOT, "residential", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(p))
        print("wrote", os.path.relpath(os.path.join(d, "index.html"), ROOT))
    patch_home()
    print("patched index.html")


if __name__ == "__main__":
    main()
