# Pravi sajt/ (SR i EN stranicu) iz dizajna mechanically-gifted-tech.html.
# Pokretanje: python napravi-sajt.py   (posle toga: napravi-slike.ps1 za PNG slike)
import html, json, os, re

DOMEN = "https://mechanicallygifted.rs"
EMAIL = "mechanicallygifted97@gmail.com"
TEL_PRIKAZ = "+381 69 3329 029"
TEL = "+381693329029"
GA_ID = "G-STL2YKYT85"
# Google recenzije: link iz "Zatražite recenzije" (Google Business) i profil na Google Mapama
RECENZIJA_LINK = "https://g.page/r/CS8wyzo--3KAEBM/review"
MAPE_LINK = "https://maps.google.com/?cid=9255736428892729391"
# Politika privatnosti po jeziku
PRIVATNOST = {"sr": "/privatnost/", "en": "/en/privacy/"}
LINKOVI = {
    "Eskay Products": "https://eskayproducts.com/",
    "Majstori Pazova": "https://majstoripazova.rs/",
    "GitHub": "https://github.com/MilosG997",
    "QA": "https://github.com/MilosG997/qa-automation",
}
from portfolio import FOLDERI, jezik, velicine
VELICINE = velicine()  # dimenzije slika iz sajt/img/portfolio (pravi ih portfolio.py)

TU = os.path.dirname(os.path.abspath(__file__))
IZLAZ = os.path.join(TU, "sajt")
izvor = open(os.path.join(TU, "dizajn.html"), encoding="utf-8").read()

# Rečnik prevoda iz JS-a u fajlu
m = re.search(r"const T=\{en:(\{.*?\}),sr:(\{.*?\})\};", izvor, re.S)
T = {"en": json.loads(m.group(1)), "sr": json.loads(m.group(2))}

# Fontovi (OFL licenca, sajt/fonts; prave ih napravi-fontove.py). Naslovni serif (i kosi) i tekstualni font su
# UGRAĐENI u stranicu (base64): naslov i uvodni pasus odmah imaju pravi font, bez čekanja na mrežu. Mono (sitne
# oznake) se preuzima posebno, sa swap, pa ne zadržava prikaz. Svaki fajl ima latinicu i srpska slova.
FONTOVI = [  # (porodica, fajl, stil, debljina, ugrađen)
    ("MG Serif", "mg-serif", "normal", "400", True),
    ("MG Serif", "mg-serif-i", "italic", "400", True),
    ("MG Sans", "mg-sans", "normal", "400 700", True),
    ("MG Mono", "mg-mono", "normal", "450", False),
]


def fontovi(jez):
    import base64
    out = []
    for ime, fajl, stil, tezina, ugradi in FONTOVI:
        put = os.path.join(TU, "sajt", "fonts", fajl + ".woff2")
        src = ("url(data:font/woff2;base64," + base64.b64encode(open(put, "rb").read()).decode() + ")") if ugradi \
            else f"url(/fonts/{fajl}.woff2)"
        out.append(f'@font-face{{font-family:"{ime}";font-style:{stil};font-weight:{tezina};font-display:swap;'
                   f'src:{src} format("woff2")}}\n')
    return "".join(out)


css = open(os.path.join(TU, "stil.css"), encoding="utf-8").read()

telo = re.search(r"(<header>.*?</footer>)", izvor, re.S).group(1)


def stranica(jez):
    t = T[jez]
    b = telo

    def zameni(mm):
        kljuc = mm.group(3)
        tekst = html.escape(t[kljuc], quote=False) if kljuc in t else mm.group(5)
        return mm.group(1) + mm.group(4) + tekst + mm.group(6)

    b = re.sub(r'(<(\w+)[^>]*?)\sdata-i18n="([^"]+)"([^>]*>)([^<]*)(</\2>)', zameni, b)

    # SR / EN kao obični linkovi
    sr_akt = ' aria-current="page"' if jez == "sr" else ""
    en_akt = ' aria-current="page"' if jez == "en" else ""
    b = re.sub(r'<div class="lang".*?</div>',
               f'<div class="lang" role="group" aria-label="Jezik / Language">'
               f'<a href="/" hreflang="sr" lang="sr"{sr_akt}>SR</a>'
               f'<a href="/en/" hreflang="en" lang="en"{en_akt}>EN</a></div>', b, count=1, flags=re.S)

    # O meni posle Usluga (pre "Kako radim"), plus link u meniju
    assert b.count('<section class="koraci">') == 1
    b = b.replace('<section class="koraci">', omeni_html(jez) + '<section class="koraci">', 1)
    b, n = re.subn(r'<nav class="links"[^>]*><a [^>]*href="#usluge">[^<]*</a>', lambda m: m.group(0) + '<a href="#omeni">' + OMENI[jez]["nav"] + "</a>", b, count=1)
    assert n == 1
    # Delovi koje pravi Python: nacrt zupčanika, oznaka QA skena, alati, velika traka teksta; 3D modul sa verzijom
    for oznaka, deo in (("<!--NACRT-->", NACRT), ("<!--SKEN-->", sken_html(jez)), ("<!--ALATI-->", alati_html(jez)),
                        ):
        assert b.count(oznaka) == 1, oznaka
        b = b.replace(oznaka, deo, 1)
    b = b.replace('<div class="scena" aria-hidden="true"></div>', f'<div class="scena" aria-hidden="true" data-js="{HERO3D}"></div>', 1)
    # Recenzije sa Google-a iznad FAQ-a (podrazumevano mala traka; JS je zameni karticama kad ih ima)
    assert '<section id="pitanja">' in b
    b = b.replace('<section id="pitanja">', recenzije_html(jez) + '<section id="pitanja">', 1)

    # Portfolio: folderi iz portfolio.py
    assert "<!--PORTFOLIO-->" in b
    b = b.replace("<!--PORTFOLIO-->", portfolio_html(jez), 1)

    # Podnožje: veliko, u tonovima zaglavlja (podnozje_html)
    b, n = re.subn(r"<footer>.*?</footer>", lambda mm: podnozje_html(jez), b, count=1, flags=re.S)
    assert n == 1

    # Kontakt: mailto, tel, bez LinkedIn-a, Viber i WhatsApp dugmad
    b = b.replace('<span id="v0">kontakt@mechanicallygifted.rs</span>',
                  f'<span id="v0"><a href="mailto:{EMAIL}">{EMAIL}</a></span>')
    b = b.replace('<span id="v1">+381 6X XXX XXXX</span>',
                  f'<span id="v1"><a href="tel:{TEL}">{TEL_PRIKAZ}</a></span>')
    assert b.count("<!--APPS-->") == 1
    b = b.replace("<!--APPS-->", '<div class="apps">'
                  f'<a class="btn btn-l" href="viber://chat?number=%2B{TEL[1:]}">Viber</a>'
                  f'<a class="btn btn-l" href="https://wa.me/{TEL[1:]}" target="_blank" rel="noopener">WhatsApp</a>'
                  '</div>', 1)
    if jez == "en":  # ova oznaka nije bila u rečniku
        b = b.replace("<small>Telefon · Viber · WhatsApp</small>", "<small>Phone · Viber · WhatsApp</small>")
    b = b.replace("</main>", "</main>\n" + galerija_json(jez), 1)
    return IKONICE + b


# Ikonice alata: Simple Icons 16.35.0 (CC0, izvor-ikonica/*.svg) + tri nacrtane ovde (Liquid, Klaviyo, Photoshop).
# Boje su boje brendova (svetlije gde bi se na tamnoj podlozi izgubile); vide se kad se pređe mišem.
ALATI = {  # ime: (ikonica, boja)
    "Shopify": ("shopify", "#7AB55C"), "Liquid": ("liquid", "#95BF47"), "HTML": ("html5", "#E34F26"),
    "CSS": ("css", "#9B6BDF"), "JavaScript": ("javascript", "#F7DF1E"), "Python": ("python", "#5A9FD4"),
    "Java": ("openjdk", "#F89820"), "Git": ("git", "#F05032"), "GitHub": ("github", "#FFFFFF"),
    "Netlify": ("netlify", "#00C7B7"), "Firebase": ("firebase", "#FFCA28"), "WooCommerce": ("woocommerce", "#B07CAB"),
    "Selenium": ("selenium", "#43B02A"), "Pytest": ("pytest", "#0A9EDC"), "Appium": ("appium", "#EE376D"),
    "Postman": ("postman", "#FF6C37"), "GitHub Actions": ("githubactions", "#2088FF"), "Klaviyo": ("klaviyo", "#F2F2F2"),
    "Figma": ("figma", "#F24E1E"), "Photoshop": ("photoshop", "#31A8FF"), "Google Analytics": ("googleanalytics", "#E37400"),
    "Search Console": ("googlesearchconsole", "#458CF5"), "SEO": ("googlesearchconsole", "#458CF5"),
}
RED_ALATA = [["Shopify", "Liquid", "HTML", "CSS", "JavaScript", "Python", "Java", "Git", "GitHub", "Netlify", "Firebase", "WooCommerce"],
             ["Selenium", "Pytest", "Appium", "Postman", "GitHub Actions", "Klaviyo", "Figma", "Photoshop", "Google Analytics", "Search Console"]]
NACRTANE = {
    "liquid": '<path fill-rule="evenodd" d="M12 2.2c.3 0 .5.1.7.4 3.1 4.3 6.3 8.3 6.3 12a7 7 0 0 1-14 0c0-3.7 3.2-7.7 6.3-12 .2-.3.4-.4.7-.4zm-3.2 12.3c-.5 0-.9.4-.9.9a4.2 4.2 0 0 0 4.1 4.2c.5 0 .9-.4.9-.9s-.4-.9-.9-.9c-1.3 0-2.3-1.1-2.3-2.4 0-.5-.4-.9-.9-.9z"/>',
    "klaviyo": '<path d="M2.5 3.5h19l-5.2 8.5 5.2 8.5h-19z"/>',
    "photoshop": '<rect x="2" y="2" width="20" height="20" rx="4.5"/><text x="12" y="16.2" text-anchor="middle" font-family="MG Mono,monospace" font-size="9.5" fill="#050a1a">Ps</text>',
}


def _ikonica(slug):
    if slug in NACRTANE:
        return NACRTANE[slug]
    svg = open(os.path.join(TU, "izvor-ikonica", slug + ".svg"), encoding="utf-8").read()
    return f'<path d="{re.search(r"<path d=\"([^\"]+)\"", svg).group(1)}"/>'


IKONICE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
           + "".join(f'<symbol id="i-{slug}" viewBox="0 0 24 24">{_ikonica(slug)}</symbol>'
                     for slug in sorted({v[0] for v in ALATI.values()})) + "</svg>\n")
ALATI_TEKST = {"sr": ("Alati sa kojima radim", "{n} alata"), "en": ("Tools I work with", "{n} tools")}


def alati_html(jez):
    """Dve trake logotipa koje teku u suprotnim smerovima; svaka traka je 3 puta ista (bez praznine na širokom ekranu)."""
    naslov, broj = ALATI_TEKST[jez]
    stavka = lambda ime: (f'<span class="alat" style="--c:{ALATI[ime][1]}"><svg aria-hidden="true">'
                          f'<use href="#i-{ALATI[ime][0]}"/></svg>{html.escape(ime)}</span>')
    redovi = []
    for i, red in enumerate(RED_ALATA):
        jedan = "".join(stavka(x) for x in red)
        redovi.append(f'<div class="mq{" mq-r" if i else ""}"><div class="mq-in">{jedan}</div>'
                      f'<div class="mq-in" aria-hidden="true">{jedan}</div><div class="mq-in" aria-hidden="true">{jedan}</div></div>')
    ukupno = sum(len(r) for r in RED_ALATA)
    return (f'<div class="alati" role="region" aria-label="{naslov}"><div class="w alati-zag"><span class="eye">{naslov}</span>'
            f'</div>{"".join(redovi)}</div>')


VELIKI = {"sr": ["Shopify", "Web dizajn", "QA testiranje", "SEO", "Sajtovi"],
          "en": ["Shopify", "Web design", "QA testing", "SEO", "Websites"]}


def veliki_html(jez):
    reci = "".join(f"<span>{w}</span><b>✦</b>" for w in VELIKI[jez])
    return f'<div class="veliki" aria-hidden="true"><div class="veliki-in">{reci * 3}</div></div>'


SKEN = {"sr": {"pre": "QA sken · spreman", "radi": "QA sken {n} · proverava…", "prosao": "QA sken {n} · PASS ✓"},
        "en": {"pre": "QA scan · ready", "radi": "QA scan {n} · running…", "prosao": "QA scan {n} · PASS ✓"}}


def sken_html(jez):
    t = SKEN[jez]
    return f'<span class="sken" aria-hidden="true" data-radi="{t["radi"]}" data-prosao="{t["prosao"]}">{t["pre"]}</span>'


def nacrt_svg():
    """Plavi nacrt zupčanika: iscrta se odmah (bez JS-a), a kad se 3D učita ostaje kao bled crtež iza metala."""
    import math

    def zupcanik(cx, cy, n, s, sektori=0):
        m = 0.16 * s
        rp, k = m * n / 2, 2 * math.pi / n
        ra, rf = rp + m, rp - 1.25 * m
        P = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))  # noqa: E731
        f = lambda p: f"{p[0]:.1f} {p[1]:.1f}"  # noqa: E731
        d = ""
        for i in range(n):
            a = i * k
            d += ("M" if i == 0 else "L") + f(P(rf, a - k * .27)) + "Q" + f(P(rp, a - k * .25)) + " " + f(P(ra, a - k * .13))
            d += "L" + f(P(ra, a + k * .13)) + "Q" + f(P(rp, a + k * .25)) + " " + f(P(rf, a + k * .27))
        el = [f'<path class="lin" pathLength="1" d="{d}Z"/>',
              f'<circle class="lin tank" cx="{cx:.1f}" cy="{cy:.1f}" r="{rp:.1f}"/>']
        if sektori:
            r1, r2, sir, krak = rp * .42, rf - rp * .16, 2 * math.pi / sektori, .24 * s / rp
            for i in range(sektori):
                a0, a1 = i * sir + krak, (i + 1) * sir - krak
                el.append(f'<path class="lin" pathLength="1" d="M{f(P(r2, a0))}A{r2:.1f} {r2:.1f} 0 0 1 {f(P(r2, a1))}'
                          f'L{f(P(r1, a1))}A{r1:.1f} {r1:.1f} 0 0 0 {f(P(r1, a0))}Z"/>')
        return el, ra

    cx, cy, s = 330, 320, 92
    g1, ra1 = zupcanik(cx, cy, 30, s, sektori=6)
    g1 += [f'<circle class="lin" pathLength="1" cx="{cx}" cy="{cy}" r="{1.06 * s:.1f}"/>',
           f'<circle class="lin" pathLength="1" cx="{cx}" cy="{cy}" r="{.32 * s:.1f}"/>']
    ugao, d = -0.62, (0.16 * 30 / 2 + 0.16 * 14 / 2) * s
    x2, y2 = cx + d * math.cos(ugao), cy + d * math.sin(ugao)
    g2, ra2 = zupcanik(x2, y2, 14, s)
    g2 += [f'<circle class="lin" pathLength="1" cx="{x2:.1f}" cy="{y2:.1f}" r="{.16 * s:.1f}"/>']
    mere = [  # osne linije, kotna linija prečnika, oznake
        f'<path class="lin tank" d="M{cx - ra1 - 60} {cy}H{x2 + ra2 + 40}M{cx} {cy - ra1 - 50}V{cy + ra1 + 70}"/>',
        f'<path class="lin" pathLength="1" d="M{cx - ra1:.1f} {cy + ra1 + 40:.1f}H{cx + ra1:.1f}M{cx - ra1:.1f} {cy + ra1 + 32:.1f}v16M{cx + ra1:.1f} {cy + ra1 + 32:.1f}v16"/>',
        f'<text class="mera" x="{cx}" y="{cy + ra1 + 32:.1f}" text-anchor="middle">Ø {2 * ra1:.0f} · Z 30 · m 0.16</text>',
        f'<text class="mera" x="{x2 + ra2 + 14:.1f}" y="{y2 - ra2:.1f}">DETALJ A · Z 14</text>',
        f'<text class="mera" x="{cx - ra1 - 60}" y="{cy - 12}">MG-01 / A–A</text>',
    ]
    return (f'<svg viewBox="0 0 680 680" aria-hidden="true" focusable="false"><g class="okret">{"".join(g1)}</g>'
            f'<g class="okret2" style="transform-origin:{x2:.1f}px {y2:.1f}px">{"".join(g2)}</g>{"".join(mere)}</svg>')


NACRT = nacrt_svg()
# 3D modul (3d/: npm run build) sa verzijom u adresi, da pregledač uzme novi čim se promeni
import hashlib  # noqa: E402
HERO3D = "/js/hero3d.js?v=" + hashlib.md5(open(os.path.join(TU, "sajt", "js", "hero3d.js"), "rb").read()).hexdigest()[:10]

PODNOZJE = {"sr": {"kontakt": "Kontakt", "odgovor": "Odgovaram isti dan.", "sajt": "Sajt", "linkovi": "Linkovi",
                   "vrh": "Na vrh ↑", "priv": "Privatnost", "drugi": ('/en/', "en", "English")},
            "en": {"kontakt": "Contact", "odgovor": "I reply the same day.", "sajt": "Site", "linkovi": "Links",
                   "vrh": "Back to top ↑", "priv": "Privacy", "drugi": ("/", "sr", "Srpski")}}


def podnozje_html(jez):
    """Podnožje u tonovima zaglavlja: kontakt, meni, linkovi, veliki natpis i donja traka."""
    t, P = T[jez], PODNOZJE[jez]
    meni = [("#usluge", t["nav.s"]), ("#omeni", OMENI[jez]["nav"]), ("#radovi", t["nav.w"]), ("#pitanja", t["nav.f"]),
            ("#kontakt", t["nav.c"])]
    url, hl, ime = P["drugi"]
    usluge = re.sub(r" · (Srbija|Serbia)$", "", t["ft"])
    return (f'<footer><div class="w"><div class="ft-top"><div class="ft-brend"><b>Mechanically <em>Gifted</em></b>'
            f'<span>{html.escape(usluge)}</span></div>'
            f'<nav class="ft-kol" aria-label="{P["sajt"]}"><h4>{P["sajt"]}</h4>'
            + "".join(f'<a href="{h}">{html.escape(x)}</a>' for h, x in meni) + '</nav>'
            f'<nav class="ft-kol" aria-label="{P["linkovi"]}"><h4>{P["linkovi"]}</h4><a href="mailto:{EMAIL}">Email</a>'
            f'<a href="{LINKOVI["GitHub"]}" target="_blank" rel="noopener">GitHub</a>'
            f'<a href="{url}" hreflang="{hl}" lang="{hl}">{ime}</a><a href="{PRIVATNOST[jez]}">{P["priv"]}</a></nav></div></div>'
            f'<div class="w ft-bot"><span>© 2026 Mechanically Gifted</span>'
            f'<a class="na-vrh" href="#top">{P["vrh"]}</a></div></footer>')


RECENZIJE = {
    "sr": {"lang": "sr", "eye": "Recenzije", "naslov": "Šta kažu klijenti", "svi": "Pogledaj sve na Google-u",
           "ostavi": "★ Ostavi recenziju", "cnt1": "na osnovu {n} recenzije na Google-u",
           "cnt5": "na osnovu {n} recenzija na Google-u", "vise": "Prikaži još", "manje": "Prikaži manje",
           "link": "Pogledaj na Google-u →", "izvor": "Recenzije sa Google-a", "pre": "Prethodne", "sled": "Sledeće",
           "ocena": "Ocena {n} od 5", "poziv": "Radili ste sa mnom? Ostavite recenziju na Google-u"},
    "en": {"lang": "en", "eye": "Reviews", "naslov": "What clients say", "svi": "See all on Google",
           "ostavi": "★ Leave a review", "cnt1": "based on {n} review on Google",
           "cnt5": "based on {n} reviews on Google", "vise": "Show more", "manje": "Show less",
           "link": "View on Google →", "izvor": "Reviews from Google", "pre": "Previous", "sled": "Next",
           "ocena": "Rated {n} out of 5", "poziv": "Worked with me? Leave a review on Google"},
}
OMENI = {
    "sr": {"nav": "O meni", "naslov": "Zdravo, ja sam Miloš", "uloga": "QA Automation Engineer · Shopify Specialist · Web Developer",
           "klik": "Klikni da me upoznaš",
           "p": ["Upoznaj čoveka iza Mechanically Gifted. Ja sam onaj koji pravi sajtove, sređuje Shopify prodavnice i piše testove.",
                 "U IT-ju sam više od 10 godina. Krenuo sam 2015. kao freelancer: web dizajn u Figmi i Photoshopu, Shopify i WooCommerce prodavnice i SEO. Svaki projekat mi je doneo novo znanje.",
                 "Kroz testiranje sajtova i igrica našao sam svoje mesto u QA-u. Danas pišem automatske testove u Selenium-u, Appium-u, Pytest-u i Postman-u (Python i Java) za web, mobilne aplikacije i API. Radim samostalno, držim se rokova i ništa ne puštam uživo dok ga ne istestiram."],
           "kraj": "Nekada sam maštao da postanem profesionalni fudbaler, a postao sam QA inženjer... Nije loše.",
           "alati": [("Testiranje", ["Selenium", "Appium", "Pytest", "Postman"]),
                     ("Razvoj", ["Python", "Java", "HTML", "CSS", "Liquid", "Git"]),
                     ("E-commerce i dizajn", ["Shopify", "WooCommerce", "Klaviyo", "Figma", "Photoshop", "SEO"])],
           "razgovor": "Hajde da popričamo", "radovi": "Pogledaj radove →"},
    "en": {"nav": "About", "naslov": "Hi, I'm Miloš", "uloga": "QA Automation Engineer · Shopify Specialist · Web Developer",
           "klik": "Click to get to know me",
           "p": ["Meet the person behind Mechanically Gifted. I'm the one who builds the websites, sets up the Shopify stores and writes the tests.",
                 "I've been in IT for more than 10 years. I started in 2015 as a freelancer: web design in Figma and Photoshop, Shopify and WooCommerce stores, and SEO. Every project taught me something new.",
                 "Testing websites and games is how I found my place in QA. Today I write automated tests with Selenium, Appium, Pytest and Postman (Python and Java) for the web, mobile apps and APIs. I work on my own, I stick to deadlines, and nothing goes live until I've tested it."],
           "kraj": "I used to dream of becoming a professional footballer. I became a QA engineer instead... Not bad.",
           "alati": [("Testing", ["Selenium", "Appium", "Pytest", "Postman"]),
                     ("Development", ["Python", "Java", "HTML", "CSS", "Liquid", "Git"]),
                     ("E-commerce & design", ["Shopify", "WooCommerce", "Klaviyo", "Figma", "Photoshop", "SEO"])],
           "razgovor": "Let's talk", "radovi": "See my work →"},
}


def omeni_html(jez):
    """Sekcija O meni: zatvorena kartica sa slikom, klik otvara tekst i alate (čipovi sa ikonicama)."""
    L, e = OMENI[jez], (lambda x: html.escape(x, quote=False))
    p = f'<p class="lead">{e(L["p"][0])}</p>' + "".join(f"<p>{e(x)}</p>" for x in L["p"][1:])
    uloga = " · ".join(e(x).replace(" ", "&nbsp;") for x in L["uloga"].split(" · "))  # lomi se samo na tačkici
    cip = lambda ime: (f'<span class="cip"><svg aria-hidden="true"><use href="#i-{ALATI[ime][0]}"/></svg>{e(ime)}</span>'
                       if ime in ALATI else f'<span class="cip">{e(ime)}</span>')
    alati = "".join(f"<div><h4>{e(h)}</h4><p>{''.join(cip(x) for x in imena)}</p></div>" for h, imena in L["alati"])
    return (f'<section id="omeni" class="omeni"><div class="w"><div class="sh" data-r><div class="eye" data-n="02">{e(L["nav"])}</div></div>'
            f'<div class="ab">'
            f'<button type="button" class="abhead" id="abBtn" aria-expanded="false" aria-controls="abBody">'
            f'<span class="av"><span class="ring"></span><span class="pic"><img src="/img/milos.webp" alt="Miloš Grbović" '
            f'width="240" height="240" loading="lazy" decoding="async"></span></span>'
            f'<span class="abt"><b>{e(L["naslov"])}</b><span>{uloga}</span><em>{e(L["klik"])}</em></span>'
            f'<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
            f'</button><div class="abbody" id="abBody" role="region" aria-labelledby="abBtn" inert><div class="abin"><div class="abpad">'
            f'<div class="atxt">{p}<p class="end">{e(L["kraj"])}</p></div><div class="tools">{alati}</div>'
            f'<div class="ab-cta"><a class="btn btn-g sm" href="#kontakt">{e(L["razgovor"])}</a>'
            f'<a class="btn btn-l sm" href="#radovi">{e(L["radovi"])}</a></div>'
            f'</div></div></div></div></div></section>\n')


OMENI_JS = ('(()=>{const b=document.getElementById("abBtn");if(!b)return;const a=b.closest(".ab"),t=document.getElementById("abBody");'
            'b.addEventListener("click",()=>{const o=!a.classList.contains("open");a.classList.toggle("open",o);'
            'b.setAttribute("aria-expanded",o);t.inert=!o})})();')


# Recenzije prepisane sa Google profila (dok Places API ključ nije podešen). Tekst u originalu, kako je napisan.
# Nova recenzija: dodaj stavku, ažuriraj ocenu/broj sa profila, pa napravi i objavi sajt.
RUCNE_RECENZIJE = {
    "rating": 5.0, "userRatingCount": 8,
    "reviews": [
        {"author": "Jovan Sindjelic", "rating": 5, "lang": "sr",
         "text": "Brza i profesionalna usluga, odlična saradnja i sve po dogovoru. Sve preporuke!",
         "photo": "https://lh3.googleusercontent.com/a/ACg8ocKIw0CTvEzUR4tH4XgdjT-thgy0v9fLZtjgwOI27uHJtjkpwg=w84-h84-p-rp-mo-br100",
         "time": {"sr": "oktobar 2026.", "en": "October 2026"}},
        {"author": "Goran Bošković", "rating": 5, "lang": "sr",
         "text": "Bavim se sličnim stvarima i želim da preporučim momka i firmu koja se bavi mojim poslom 🙂…",
         "time": {"sr": "oktobar 2026.", "en": "October 2026"}},
        {"author": "Dragan Kantar", "rating": 5, "lang": "sr",
         "text": "Licno vec duze vremena imam saradnju sa deckom cija je ovo prica na nekim drugim poslovima, tako da verujem da ce i ovde ave da bude kako treba. Podrska od mene i sve preporuke.",
         "photo": "https://lh3.googleusercontent.com/a/ACg8ocLLBQOQzyPU-Ze8ZZ0UBEgv_-ukNkKJgBWtnBH8ZzGn7wLiZw=w84-h84-p-rp-mo-br100",
         "time": {"sr": "oktobar 2026.", "en": "October 2026"}},
        {"author": "Sladjana Bosnic", "rating": 5, "lang": "sr",
         "text": "Imala sam vec jednu saradnju sa ovom firmom i za sada nemam zamerki, sve pohvale.",
         "photo": "https://lh3.googleusercontent.com/a/ACg8ocIfcW4tHCIyvKISespo6x0DAhmI5YsnJ7YvrhLINU5NG2NgGA=w84-h84-p-rp-mo-br100",
         "time": {"sr": "oktobar 2026.", "en": "October 2026"}},
        {"author": "Božidar Božović", "rating": 5, "lang": "bs", "text": "Podrška za nove inovacije 💪…",
         "photo": "https://lh3.googleusercontent.com/a/ACg8ocKrStb9IZz1tF8n9056qfGnoLW_v6Mq58u_J_5kGyQyQD8TAA=w84-h84-p-rp-mo-br100",
         "time": {"sr": "oktobar 2026.", "en": "October 2026"}},
    ],
}


def rucne_recenzije(jez):
    d = dict(RUCNE_RECENZIJE, mapsUri=MAPE_LINK)
    d["reviews"] = [dict(r, time=r["time"][jez], link=MAPE_LINK) for r in RUCNE_RECENZIJE["reviews"]]
    return d


GOOGLE_G = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="revG" viewBox="0 0 48 48">'
            '<path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.9 6.1C12.5 13.6 17.8 9.5 24 9.5z"/>'
            '<path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.8c4.3-4 6.9-9.9 6.9-17.2z"/>'
            '<path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.1C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7l7.9-6.1z"/>'
            '<path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.8c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.9l-7.9 6.1C6.6 42.6 14.6 48 24 48z"/>'
            '</symbol></svg>')


def recenzije_html(jez):
    """Mala traka "Ostavite recenziju" u HTML-u; recenzije.js je zameni celom sekcijom kad API vrati recenzije."""
    L = RECENZIJE[jez]
    e = lambda x: html.escape(x, quote=True)
    ostavi = RECENZIJA_LINK or "#"
    mape = MAPE_LINK or "#"
    return (f'{GOOGLE_G}<section id="recenzije" class="rev-sec rev-mala" data-tekst="{e(json.dumps(L, ensure_ascii=False))}" '
            f'data-rucno="{e(json.dumps(rucne_recenzije(jez), ensure_ascii=False))}">'
            f'<div class="w"><div class="rev-sum">'
            f'<div class="rev-poziv"><div class="rev-g"><svg width="24" height="24" aria-hidden="true"><use href="#revG"/></svg></div>'
            f'<span>{e(L["poziv"])}</span></div><div class="rev-acts">'
            f'<a class="btn btn-l rev-svi" href="{e(mape)}" target="_blank" rel="noopener">{e(L["svi"])}</a>'
            f'<a class="btn btn-g rev-ostavi" href="{e(ostavi)}" target="_blank" rel="noopener">{e(L["ostavi"])}</a>'
            f'</div></div></div></section>\n')


REC = {"sr": {"pogledaj": "Pogledaj", "dizajn": "Pogledaj dizajn"},
       "en": {"pogledaj": "View", "dizajn": "View design"}}
# Ikonica foldera iz odobrenog demo dizajna (prednja strana se otvara, papir izlazi)
IKONA = ('<span class="ico" aria-hidden="true"><svg viewBox="0 0 52 42"><path class="back" d="M2 6a4 4 0 0 1 4-4h13l5 5h22'
         'a4 4 0 0 1 4 4v27a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><rect class="paper" x="8" y="10" width="36" height="22" rx="2"/>'
         '<path class="front" d="M2 15a4 4 0 0 1 4-4h40a4 4 0 0 1 4 4v23a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/></svg></span>')
STRELICA = ('<svg class="chev" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round"><path d="M6 9l6 6 6-6"/></svg>')


def portfolio_html(jez):
    """Četiri foldera (zatvoreni na početku); stavke su u HTML-u radi Google-a, a inert dok je folder zatvoren."""
    e = lambda x: html.escape(x, quote=True)
    rec = REC[jez]
    out = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="mgFolder" '
           'x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f5bff"/><stop offset="1" stop-color="#59c3ff"/>'
           '</linearGradient></defs></svg><div class="folders">']
    for f in FOLDERI:
        k = f["key"]
        stat = (f'<p class="f-stat"><b>{e(f["stat"][jez][0])}</b> {e(f["stat"][jez][1])}</p>' if "stat" in f else "")
        stavke = []
        for s_ in f["stavke"]:
            naslov = jezik(s_["naslov"], jez)
            slika = (f'<img class="thumb" src="/img/portfolio/{s_["slug"]}-thumb.webp" alt="{e(s_["alt"][jez])}" '
                     f'width="480" height="300" loading="lazy" decoding="async">')
            if s_.get("lightbox"):
                akcija = f'<button type="button" class="vise" data-lb="{s_["slug"]}">{rec["dizajn"]}</button>'
            else:
                tekst = jezik(s_.get("link_tekst", {"sr": f'{rec["pogledaj"]} {naslov}', "en": f'{rec["pogledaj"]} {naslov}'}), jez)
                akcija = f'<a href="{s_["link"]}" target="_blank" rel="noopener">{e(tekst)}</a>'
            oznaka = f'<small class="oznaka">{e(s_["oznaka"][jez])}</small>' if "oznaka" in s_ else ""
            stavke.append(f'<div class="item">{slika}<div><h3>{e(naslov)}</h3>{oznaka}'
                          f'<p>{e(s_["opis"][jez])}</p>{akcija}</div></div>')
        out.append(
            f'<div class="f" data-folder="{k}"><button type="button" class="head" id="fh-{k}" aria-expanded="false" '
            f'aria-controls="fb-{k}">{IKONA}<span class="t"><b>{e(f["naziv"][jez])}</b><span>{e(f["opis"][jez])}</span></span>'
            f'<span class="cnt">{len(f["stavke"])}</span>{STRELICA}</button>'
            f'<div class="body" id="fb-{k}" role="region" aria-labelledby="fh-{k}" inert><div class="inner">'
            f'{stat}<div class="list">{"".join(stavke)}</div></div></div></div>')
    out.append("</div>")
    return "".join(out)


LIGHTBOX = {"sr": {"zatvori": "Zatvori", "pre": "Prethodni rad", "sled": "Sledeći rad"},
            "en": {"zatvori": "Close", "pre": "Previous project", "sled": "Next project"}}


def galerija_json(jez):
    """Podaci za lightbox (samo Web dizajn). Sam prozor pravi JS tek pri prvom otvaranju."""
    dizajn = next(f for f in FOLDERI if f["key"] == "dizajn")
    radovi = {s_["slug"]: {"naslov": jezik(s_["naslov"], jez), "opis": s_["opis"][jez], "oznaka": s_["oznaka"][jez],
                           "alt": s_["alt"][jez], "tool": "Figma",
                           "slike": [[f'/img/portfolio/{s_["slug"]}-{n + 1}.webp', w, h]
                                     for n, (w, h) in enumerate(VELICINE[s_["slug"]])]}
              for s_ in dizajn["stavke"]}
    data = {"radovi": radovi, "red": [s_["slug"] for s_ in dizajn["stavke"]], "tekst": LIGHTBOX[jez]}
    return f'<script type="application/json" id="galerija">{json.dumps(data, ensure_ascii=False)}</script>'


def faq(jez):
    t = T[jez]
    return [{"@type": "Question", "name": t[f"q{i}"],
             "acceptedAnswer": {"@type": "Answer", "text": t[f"a{i}"]}} for i in range(1, 5)]


META = {
    "sr": {
        "title": "Mechanically Gifted – Izrada sajtova, Shopify i QA testiranje",
        "desc": "Izrada sajtova, Shopify prodavnica i QA automatsko testiranje. Mechanically Gifted radi za klijente iz Srbije i inostranstva. Besplatna procena projekta.",
        "url": DOMEN + "/", "locale": "sr_RS", "alt_locale": "en_US",
        "usluga": "Izrada sajtova, Shopify dizajn i programiranje, QA automatsko testiranje.",
        "og_alt": "Mechanically Gifted – izrada sajtova, Shopify i QA testiranje",
    },
    "en": {
        "title": "Mechanically Gifted – Shopify, Web Design & QA Automation",
        "desc": "Shopify development, websites for small businesses and automated QA testing with Selenium. Working with clients in Serbia and abroad. Free project quote.",
        "url": DOMEN + "/en/", "locale": "en_US", "alt_locale": "sr_RS",
        "usluga": "Shopify design and development, simple websites, QA test automation.",
        "og_alt": "Mechanically Gifted – Shopify development, web design and QA automation",
    },
}


def glava(jez, k=None, noindex=False, par=("/", "/en/"), ld=None):
    """par = (srpska putanja, engleska putanja) iste stranice, za hreflang; ld = drugi JSON-LD."""
    k = k or META[jez]
    ld_strana = ld
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": DOMEN + "/#firma", "name": "Mechanically Gifted",
         "url": k["url"], "description": k["usluga"], "email": EMAIL, "telephone": TEL,
         "logo": DOMEN + "/icon-512.png", "image": DOMEN + "/og-image.png",
         "address": {"@type": "PostalAddress", "addressCountry": "RS"},
         "areaServed": [{"@type": "Country", "name": "Srbija" if jez == "sr" else "Serbia"},
                        {"@type": "Place", "name": "Inostranstvo" if jez == "sr" else "Worldwide"}],
         "knowsLanguage": ["sr", "en"], "sameAs": [LINKOVI["GitHub"]]},
        {"@type": "FAQPage", "@id": k["url"] + "#pitanja", "inLanguage": jez, "mainEntity": faq(jez)},
    ]}
    e = lambda s: html.escape(s, quote=True)
    return f"""<!doctype html>
<html lang="{jez}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(k["title"])}</title>
<meta name="description" content="{e(k["desc"])}">{'<meta name="robots" content="noindex">' if noindex else ""}
<link rel="canonical" href="{k["url"]}">
<link rel="alternate" hreflang="sr" href="{DOMEN}{par[0]}">
<link rel="alternate" hreflang="en" href="{DOMEN}{par[1]}">
<link rel="alternate" hreflang="x-default" href="{DOMEN}{par[0]}">
<meta name="theme-color" content="#050a1a">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mechanically Gifted">
<meta property="og:title" content="{e(k["title"])}">
<meta property="og:description" content="{e(k["desc"])}">
<meta property="og:url" content="{k["url"]}">
<meta property="og:locale" content="{k["locale"]}">
<meta property="og:locale:alternate" content="{k["alt_locale"]}">
<meta property="og:image" content="{DOMEN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(k["og_alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(k["title"])}">
<meta name="twitter:description" content="{e(k["desc"])}">
<meta name="twitter:image" content="{DOMEN}/og-image.png">
<script type="application/ld+json">{json.dumps(ld if ld_strana is None else ld_strana, ensure_ascii=False)}</script>
<script>document.documentElement.classList.add("js")</script>
<style>{fontovi(jez)}{css}</style>
</head>
<body>
"""


# GA4 kao na majstoripazova.rs: radi odmah, bez banera; gtag.js se učitava posle prvog prikaza.
# Prati samo na pravom domenu (ne lokalno). Klikovi se hvataju na jednom mestu (delegirano).
GA = """<script>
(()=>{if(location.hostname!=="mechanicallygifted.rs")return;
window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};
gtag("js",new Date());gtag("config","%(id)s",{allow_google_signals:false,allow_ad_personalization_signals:false});
const ucitaj=()=>{const s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id=%(id)s";document.head.appendChild(s)};
document.readyState==="complete"?ucitaj():addEventListener("load",ucitaj,{once:true})})();
function mgEvent(ime,param){try{window.gtag&&gtag("event",ime,Object.assign({page_language:document.documentElement.lang},param||{}))}catch(e){}}
document.addEventListener("click",e=>{const el=e.target.closest("a,button");if(!el)return;
const h=el.getAttribute("href")||"",stavka=el.closest(".folders .item");
if(h.startsWith("mailto:"))mgEvent("contact_email_click",{link_location:el.closest("footer")?"footer":"contact"});
else if(h.startsWith("tel:"))mgEvent("contact_phone_click");
else if(h.startsWith("viber:"))mgEvent("contact_viber_click");
else if(h.includes("wa.me/"))mgEvent("contact_whatsapp_click");
else if(el.dataset.copy)mgEvent("contact_copy_click",{field:el.dataset.copy==="v0"?"email":"phone"});
else if(el.matches(".ctas .btn-g")&&h.endsWith("#kontakt"))mgEvent("cta_free_quote_click");
else if(el.matches(".rev-ostavi"))mgEvent("review_leave_click",{link_location:el.closest(".rev-mala")?"strip":"reviews"});
else if(el.matches(".rev-svi"))mgEvent("review_see_all_click");
else if(el.id==="abBtn"&&el.getAttribute("aria-expanded")==="true")mgEvent("about_open");
else if(stavka)mgEvent("portfolio_item_click",{item_name:stavka.querySelector("h3").textContent,link_url:el.href||""});
else if(el.hasAttribute("hreflang"))mgEvent("language_switch",{language_to:el.getAttribute("hreflang")})});
</script>
""" % {"id": GA_ID}


PORTFOLIO_JS = open(os.path.join(TU, "portfolio.js"), encoding="utf-8").read()
RECENZIJE_JS = open(os.path.join(TU, "recenzije.js"), encoding="utf-8").read()
POKRET_JS = open(os.path.join(TU, "pokret.js"), encoding="utf-8").read()


def skripte(jez):
    t = T[jez]
    return GA + "<script>\n" + PORTFOLIO_JS + "</script><script>\n" + RECENZIJE_JS + "</script><script>" + OMENI_JS + "</script>" + """<script>
const C={copy:%s,ok:%s};
document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>{
const el=document.getElementById(b.dataset.copy);
const ok=()=>{b.textContent=C.ok;setTimeout(()=>b.textContent=C.copy,1600)};
const sel=()=>{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r)};
try{navigator.clipboard.writeText(el.textContent).then(ok,sel)}catch(e){sel()}}));
</script>""" % (json.dumps(t["c.copy"], ensure_ascii=False), json.dumps(t["c.ok"], ensure_ascii=False)) + (
        "<script>\n" + POKRET_JS + "</script>\n</body>\n</html>\n")


for jez, put in (("sr", "index.html"), ("en", os.path.join("en", "index.html"))):
    p = os.path.join(IZLAZ, put)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(glava(jez) + stranica(jez) + "\n" + skripte(jez))

LOGO = open(os.path.join(TU, "logo.svg"), encoding="utf-8").read()
with open(os.path.join(IZLAZ, "favicon.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(LOGO)

with open(os.path.join(IZLAZ, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMEN}/sitemap.xml\n")

# 404 stranice u istom dizajnu (SR na /404.html, EN na /en/404.html — vidi _redirects)
NE_POSTOJI = {
    "sr": {"title": "Stranica nije pronađena – Mechanically Gifted",
           "desc": "Ova stranica ne postoji ili je premeštena.",
           "h1": "Ova stranica ne postoji", "eye": "Greška 404",
           "p": "Link je možda pogrešan ili je stranica premeštena. Vratite se na početnu ili mi pišite direktno.",
           "home": "Nazad na početnu", "home_url": "/", "kontakt": "Kontakt", "kontakt_url": "/#kontakt"},
    "en": {"title": "Page not found – Mechanically Gifted",
           "desc": "This page does not exist or has been moved.",
           "h1": "This page doesn't exist", "eye": "Error 404",
           "p": "The link may be wrong or the page has moved. Go back to the home page or contact me directly.",
           "home": "Back to home", "home_url": "/en/", "kontakt": "Contact", "kontakt_url": "/en/#kontakt"},
}
for jez, put in (("sr", "404.html"), ("en", os.path.join("en", "404.html"))):
    n = NE_POSTOJI[jez]
    k = dict(META[jez], title=n["title"], desc=n["desc"])
    g = glava(jez, k, noindex=True)
    # 404 nema canonical, hreflang ni strukturirane podatke
    g = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", g)
    g = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", g, flags=re.S)
    cela = stranica(jez)
    zaglavlje = re.search(r"<header>.*?</header>", cela, re.S).group(0)
    # linkovi iz menija vode na početnu stranicu jezika
    zaglavlje = zaglavlje.replace('href="#', f'href="{n["home_url"]}#')
    podnozje = re.search(r"<footer>.*?</footer>", cela, re.S).group(0).replace('href="#', f'href="{n["home_url"]}#')
    podnozje = podnozje.replace(f'href="{n["home_url"]}#top"', 'href="#top"')
    telo404 = (f'{zaglavlje}\n<main id="top"><div class="hero"><div class="nacrt" aria-hidden="true">{NACRT}</div>'
               f'<div class="w hero-in"><div class="eye" data-n="404">{n["eye"]}</div><h1>{n["h1"]}</h1>'
               f'<p class="lede">{n["p"]}</p><div class="ctas">'
               f'<a class="btn btn-g" href="{n["home_url"]}">{n["home"]}</a>'
               f'<a class="btn btn-l" href="{n["kontakt_url"]}">{n["kontakt"]}</a></div></div></div></main>\n'
               f'{podnozje}\n')
    with open(os.path.join(IZLAZ, put), "w", encoding="utf-8", newline="\n") as f:
        f.write(g + telo404 + skripte(jez))

def okvir(jez, pocetna):
    """Zaglavlje i podnožje sa početne stranice; meni vodi na sekcije početne."""
    cela = stranica(jez)
    zaglavlje = re.search(r"<header>.*?</header>", cela, re.S).group(0).replace('href="#', f'href="{pocetna}#')
    podnozje = re.search(r"<footer>.*?</footer>", cela, re.S).group(0).replace('href="#', f'href="{pocetna}#')
    return zaglavlje, podnozje.replace(f'href="{pocetna}#top"', 'href="#top"')


def drugi_jezik(zaglavlje, sr_url, en_url):
    """SR/EN dugme vodi na istu stranicu na drugom jeziku."""
    zaglavlje = zaglavlje.replace('<a href="/" hreflang="sr"', f'<a href="{sr_url}" hreflang="sr"')
    return zaglavlje.replace('<a href="/en/" hreflang="en"', f'<a href="{en_url}" hreflang="en"')


def zapisi(putanja, sadrzaj):
    put = os.path.join(IZLAZ, putanja.strip("/"), "index.html")
    os.makedirs(os.path.dirname(put), exist_ok=True)
    with open(put, "w", encoding="utf-8", newline="\n") as f:
        f.write(sadrzaj)


# Politika privatnosti: kratko, samo link u podnožju
POLITIKA = {
    "sr": {"title": "Politika privatnosti – Mechanically Gifted",
           "desc": "Kako sajt mechanicallygifted.rs koristi Google Analytics i podatke iz kontakt forme.",
           "html": """<div class="datum">Važi od 16.10.2026.</div>
<h1>Politika privatnosti</h1>
<p>Sajt mechanicallygifted.rs vodi Mechanically Gifted. Za sva pitanja o podacima pišite na <a href="mailto:{email}">{email}</a>.</p>
<h2>Google Analytics</h2>
<p>Sajt koristi Google Analytics 4 da bih video koliko ljudi poseti sajt i šta ih zanima. Google pri tome beleži:</p>
<ul><li>koje stranice ste otvorili i koliko dugo ste ostali,</li><li>klikove na kontakt (email, telefon, Viber, WhatsApp) i na projekte,</li><li>vrstu uređaja i pregledača i okvirnu lokaciju (grad ili zemlju),</li><li>odakle ste došli (npr. Google pretraga ili link).</li></ul>
<p>Google Analytics za to koristi kolačiće (_ga). Ne vidim vaše ime ni IP adresu i podatke ne koristim za reklame. Podatke obrađuje Google, više na <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a>. Praćenje možete isključiti dodatkom za pregledač <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Opt-out</a> ili brisanjem kolačića.</p>
<h2>Kontakt forma i poruke</h2>
<p>Kada mi pošaljete poruku preko forme, emaila, Vibera ili WhatsApp-a, podatke koje upišete (ime, email, opis posla, budžet) koristim samo da vam odgovorim i pripremim ponudu. Poruke iz forme čuva Netlify, servis na kom je sajt. Podatke ne prodajem i ne delim ni sa kim.</p>
<h2>Vaša prava</h2>
<p>Možete tražiti da vidite, ispravite ili obrišete podatke koje imam o vama: pišite na <a href="mailto:{email}">{email}</a>.</p>"""},
    "en": {"title": "Privacy policy – Mechanically Gifted",
           "desc": "How mechanicallygifted.rs uses Google Analytics and the data you send through the contact form.",
           "html": """<div class="datum">Effective 16 October 2026</div>
<h1>Privacy policy</h1>
<p>mechanicallygifted.rs is run by Mechanically Gifted. For any question about your data, email <a href="mailto:{email}">{email}</a>.</p>
<h2>Google Analytics</h2>
<p>This site uses Google Analytics 4 to see how many people visit and what they are interested in. Google records:</p>
<ul><li>which pages you open and how long you stay,</li><li>clicks on contact links (email, phone, Viber, WhatsApp) and on projects,</li><li>device and browser type and approximate location (city or country),</li><li>where you came from (for example Google search or a link).</li></ul>
<p>Google Analytics uses cookies (_ga) for this. I do not see your name or IP address and do not use the data for advertising. The data is processed by Google, see <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a>. You can turn tracking off with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics Opt-out</a> browser add-on or by deleting cookies.</p>
<h2>Contact form and messages</h2>
<p>When you send me a message through the form, email, Viber or WhatsApp, I use what you enter (name, email, project description, budget) only to reply and prepare a quote. Form submissions are stored by Netlify, the service that hosts this site. I do not sell or share your data.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete the data I have about you: email <a href="mailto:{email}">{email}</a>.</p>"""},
}
for jez in ("sr", "en"):
    n = POLITIKA[jez]
    k = dict(META[jez], title=n["title"], desc=n["desc"], url=DOMEN + PRIVATNOST[jez])
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": n["title"], "url": k["url"],
          "inLanguage": jez, "isPartOf": {"@id": DOMEN + "/#firma"}}
    g = glava(jez, k, par=(PRIVATNOST["sr"], PRIVATNOST["en"]), ld=ld)
    zaglavlje, podnozje = okvir(jez, "/" if jez == "sr" else "/en/")
    zaglavlje = drugi_jezik(zaglavlje, PRIVATNOST["sr"], PRIVATNOST["en"])
    zapisi(PRIVATNOST[jez], g + f'{zaglavlje}\n<main id="top"><section><div class="w"><article class="prose">'
           f'{n["html"].format(email=EMAIL)}</article></div></section></main>\n{podnozje}\n' + skripte(jez))

# Sitemap: sve javne stranice u parovima (sr, en) sa hreflang
PAROVI = [("/", "/en/"), (PRIVATNOST["sr"], PRIVATNOST["en"])]
with open(os.path.join(IZLAZ, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
    for sr, en in PAROVI:
        alt = (f'    <xhtml:link rel="alternate" hreflang="sr" href="{DOMEN}{sr}"/>\n'
               f'    <xhtml:link rel="alternate" hreflang="en" href="{DOMEN}{en}"/>\n'
               f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMEN}{sr}"/>\n')
        for u in (sr, en):
            f.write(f'  <url>\n    <loc>{DOMEN}{u}</loc>\n{alt}  </url>\n')
    f.write('</urlset>\n')

# Netlify: preusmerenja, zaglavlja, manifest
with open(os.path.join(IZLAZ, "_redirects"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# www i stara netlify.app adresa -> glavni domen\n"
            f"https://www.mechanicallygifted.rs/*  {DOMEN}/:splat  301!\n"
            f"http://www.mechanicallygifted.rs/*   {DOMEN}/:splat  301!\n"
            f"https://mechanicallygifted.netlify.app/*  {DOMEN}/:splat  301!\n"
            f"# engleska 404 stranica za sve što ne postoji pod /en/\n"
            f"/en/*  /en/404.html  404\n")

with open(os.path.join(IZLAZ, "_headers"), "w", encoding="utf-8", newline="\n") as f:
    f.write("/*\n"
            "  X-Content-Type-Options: nosniff\n"
            "  X-Frame-Options: DENY\n"
            "  Referrer-Policy: strict-origin-when-cross-origin\n"
            "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
            "\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "\n/js/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "\n/img/*\n  Cache-Control: public, max-age=2592000\n"
            "\n/*.png\n  Cache-Control: public, max-age=2592000\n"
            "\n/*.ico\n  Cache-Control: public, max-age=2592000\n"
            "\n/favicon.svg\n  Cache-Control: public, max-age=2592000\n"
            "\n/site.webmanifest\n  Content-Type: application/manifest+json\n")

with open(os.path.join(IZLAZ, "site.webmanifest"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"name": "Mechanically Gifted", "short_name": "MG", "start_url": "/", "display": "browser",
               "background_color": "#050a1a", "theme_color": "#050a1a",
               "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                         {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
              f, ensure_ascii=False, indent=2)

print("Gotovo:", IZLAZ)
