# Pravi sajt/ (SR i EN stranicu) iz dizajna mechanically-gifted-tech.html.
# Pokretanje: python napravi-sajt.py   (posle toga: napravi-slike.ps1 za PNG slike)
import html, json, os, re

DOMEN = "https://mechanicallygifted.rs"
EMAIL = "mechanicallygifted@gmail.com"
TEL_PRIKAZ = "+381 69 3329 029"
TEL = "+381693329029"
GA_ID = "G-STL2YKYT85"
# Politika privatnosti po jeziku
PRIVATNOST = {"sr": "/privatnost/", "en": "/en/privacy/"}
LINKOVI = {
    "Eskay Products": "https://eskayproducts.com/",
    "Tan Ti Studio": "https://tantistudio.netlify.app/",
    "Majstori Pazova": "https://majstoripazova.rs/",
    "GitHub": "https://github.com/MilosG997",
    "QA": "https://github.com/MilosG997/qa-automation",
}
from portfolio import KATEGORIJE, RADOVI, jezik, velicine
VELICINE = velicine()  # dimenzije slika iz sajt/img/portfolio (pravi ih portfolio.py)

TU = os.path.dirname(os.path.abspath(__file__))
IZLAZ = os.path.join(TU, "sajt")
izvor = open(os.path.join(TU, "dizajn.html"), encoding="utf-8").read()

# Rečnik prevoda iz JS-a u fajlu
m = re.search(r"const T=\{en:(\{.*?\}),sr:(\{.*?\})\};", izvor, re.S)
T = {"en": json.loads(m.group(1)), "sr": json.loads(m.group(2))}

# Fontovi su na našem serveru (sajt/fonts, OFL licenca) — brže od Google Fonts i keširaju se
LAT = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
       "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
LAT_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
           "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
FONTOVI = "".join(
    f'@font-face{{font-family:"{ime}";font-style:normal;font-weight:100 900;font-display:swap;'
    f'src:url(/fonts/{fajl}-{deo}-wght-normal.woff2) format("woff2");unicode-range:{opseg}}}\n'
    for ime, fajl in (("Geist", "geist"), ("Geist Mono", "geist-mono"))
    for deo, opseg in (("latin", LAT), ("latin-ext", LAT_EXT)))
css = FONTOVI + open(os.path.join(TU, "stil.css"), encoding="utf-8").read()

telo = re.search(r"(<header>.*?</footer>)", izvor, re.S).group(1)
# "</>" se u HTML-u ne prikazuje (parser ga baci) — ikonica Shopify kartice je bila prazna
telo = telo.replace('<div class="ico"></></div>', '<div class="ico">&lt;/&gt;</div>')
# Kanvas mreže pauzira se kad hero nije na ekranu (vidi skriptu dole)


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

    # Portfolio: filteri + kartice iz portfolio.py (stare 4 kartice iz dizajna se menjaju)
    b, n = re.subn(r'<div class="work">.*?</article></div>(?=</div></section>\s*<section id="pitanja")',
                   lambda mm: portfolio_html(jez), b, count=1, flags=re.S)
    assert n == 1

    # Podnožje: email, GitHub, drugi jezik
    drugi = ('<a href="/en/" hreflang="en" lang="en">English</a>' if jez == "sr"
             else '<a href="/" hreflang="sr" lang="sr">Srpski</a>')
    b = re.sub(r'<footer><div class="w"><span>(.*?)</span><span>(.*?)</span></div></footer>',
               lambda mm: f'<footer><div class="w"><span>{mm.group(1)} · {mm.group(2)}</span><nav>'
                          f'<a href="mailto:{EMAIL}">Email</a>'
                          f'<a href="{LINKOVI["GitHub"]}" target="_blank" rel="noopener">GitHub</a>'
                          f'{drugi}<a href="{PRIVATNOST[jez]}">{"Privatnost" if jez == "sr" else "Privacy"}</a>'
                          f'</nav></div></footer>', b, flags=re.S)
    assert "<nav><a href=\"mailto" in b

    # Kontakt: mailto, tel, bez LinkedIn-a, Viber i WhatsApp dugmad
    b = b.replace('<span id="v0">kontakt@mechanicallygifted.rs</span>',
                  f'<span id="v0"><a href="mailto:{EMAIL}">{EMAIL}</a></span>')
    b = b.replace('<span id="v1">+381 6X XXX XXXX</span>',
                  f'<span id="v1"><a href="tel:{TEL}">{TEL_PRIKAZ}</a></span>')
    b = re.sub(r'<div class="c"><div><small>LinkedIn</small>.*?</button></div>', '', b, flags=re.S)
    b = b.replace('</div></div></div></section>\n</main>',
                  '<div class="apps">'
                  f'<a class="btn btn-l" href="viber://chat?number=%2B{TEL[1:]}">Viber</a>'
                  f'<a class="btn btn-l" href="https://wa.me/{TEL[1:]}" target="_blank" rel="noopener">WhatsApp</a>'
                  '</div></div></div></div></section>\n</main>', 1)
    assert "apps" in b and "LinkedIn" not in b
    if jez == "en":  # ova oznaka nije bila u rečniku
        b = b.replace("<small>Telefon · Viber · WhatsApp</small>", "<small>Phone · Viber · WhatsApp</small>")
    b = b.replace("</main>", "</main>\n" + lightbox_html(jez), 1)
    return b


def portfolio_html(jez):
    """Filteri, kartice i prazan lightbox; podaci za galeriju idu u JSON na dnu."""
    t = T[jez]
    rec = {"sr": {"pogledaj": "Pogledaj", "dizajn": "Pogledaj dizajn", "filteri": "Filtriraj radove",
                  "otvori": "Otvori galeriju"},
           "en": {"pogledaj": "View", "dizajn": "View design", "filteri": "Filter projects",
                  "otvori": "Open gallery"}}[jez]
    e = lambda x: html.escape(x, quote=True)
    ima = {r["kat"] for r in RADOVI}  # dugme samo za kategorije koje imaju bar jedan rad
    filteri = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "sve" else "false"}">'
        f'{sr if jez == "sr" else en}</button>' for k, sr, en in KATEGORIJE if k == "sve" or k in ima)
    kartice = []
    for i, r in enumerate(RADOVI):
        naslov = jezik(r["naslov"], jez)
        opis = t[r["opis_kljuc"]] if "opis_kljuc" in r else r["opis"][jez]
        chips = "".join(f'<span class="chip">{e(jezik(c, jez))}</span>' for c in r["chips"])
        w, h = 800, 450
        slika = (f'<img src="/img/portfolio/{r["slug"]}-thumb.webp" alt="{e(r["alt"][jez])}" '
                 f'width="{w}" height="{h}" loading="lazy" decoding="async">')
        if "link" in r:
            tekst = jezik(r.get("link_tekst", {"sr": f'{rec["pogledaj"]} {naslov}', "en": f'{rec["pogledaj"]} {naslov}'}), jez)
            dugme = f'<a href="{r["link"]}" target="_blank" rel="noopener">{e(tekst)}</a>'
        else:
            dugme = f'<button type="button" class="vise" data-lb="{i}">{rec["dizajn"]}</button>'
        klijent = f'<small class="klijent">{e(jezik(r["klijent"], jez))}</small>' if "klijent" in r else ""
        kartice.append(
            f'<article class="case" data-cat="{r["kat"]}">'
            f'<button type="button" class="shot" data-lb="{i}" aria-label="{rec["otvori"]}: {e(naslov)}">'
            f'{slika}<span>{e(naslov)}</span></button>'
            f'<div class="bd"><div class="chips">{chips}</div>{klijent}<p>{e(opis)}</p>{dugme}</div></article>')
    return (f'<div class="filteri" role="group" aria-label="{rec["filteri"]}">{filteri}</div>'
            f'<div class="work">{"".join(kartice)}</div>')


def galerija_json(jez):
    """Slajdovi za lightbox: jedna stavka po radu, sa svim slikama tog rada."""
    t = T[jez]
    out = []
    for r in RADOVI:
        out.append({"naslov": jezik(r["naslov"], jez),
                    "opis": t[r["opis_kljuc"]] if "opis_kljuc" in r else r["opis"][jez],
                    "alat": r["alat"], "kat": r["kat"], "alt": r["alt"][jez],
                    "slike": [[f'/img/portfolio/{r["slug"]}-{n + 1}.webp', w, h]
                              for n, (w, h) in enumerate(VELICINE[r["slug"]])]})
    return json.dumps(out, ensure_ascii=False)


LIGHTBOX = {"sr": {"zatvori": "Zatvori", "pre": "Prethodni rad", "sled": "Sledeći rad", "alat": "Alat"},
            "en": {"zatvori": "Close", "pre": "Previous project", "sled": "Next project", "alat": "Tools"}}


def lightbox_html(jez):
    L = LIGHTBOX[jez]
    return (f'<div class="lb" id="lb" role="dialog" aria-modal="true" aria-labelledby="lbNaslov" hidden>'
            f'<button type="button" class="lb-x" aria-label="{L["zatvori"]}">&times;</button>'
            f'<button type="button" class="lb-nav lb-pre" aria-label="{L["pre"]}">&#8249;</button>'
            f'<button type="button" class="lb-nav lb-sled" aria-label="{L["sled"]}">&#8250;</button>'
            f'<div class="lb-okvir"><div class="lb-slike" id="lbSlike"></div>'
            f'<div class="lb-info"><div><h3 id="lbNaslov"></h3><p id="lbOpis"></p></div>'
            f'<div class="lb-meta"><small>{L["alat"]}</small><span id="lbAlat"></span><span id="lbBroj"></span></div></div>'
            f'</div></div>'
            f'<script type="application/json" id="galerija">{galerija_json(jez)}</script>')


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
        "title": "Mechanically Gifted – Shopify Development, Web Design & QA Automation",
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
<link rel="preload" href="/fonts/geist-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/geist-mono-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{css}</style>
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
const h=el.getAttribute("href")||"",kart=el.closest(".case"),proj=kart&&kart.querySelector(".shot span");
if(h.startsWith("mailto:"))mgEvent("contact_email_click",{link_location:el.closest("footer")?"footer":"contact"});
else if(h.startsWith("tel:"))mgEvent("contact_phone_click");
else if(h.startsWith("viber:"))mgEvent("contact_viber_click");
else if(h.includes("wa.me/"))mgEvent("contact_whatsapp_click");
else if(el.dataset.copy)mgEvent("contact_copy_click",{field:el.dataset.copy==="v0"?"email":"phone"});
else if(el.matches(".ctas .btn-g")&&h.endsWith("#kontakt"))mgEvent("cta_free_quote_click");
else if(kart&&el.tagName==="A")mgEvent("portfolio_click",{project:proj?proj.textContent:"",link_url:el.href});
else if(el.hasAttribute("hreflang"))mgEvent("language_switch",{language_to:el.getAttribute("hreflang")});
else if(el.dataset.filter)mgEvent("portfolio_filter",{filter:el.dataset.filter,filter_name:el.textContent.trim()})});
</script>
""" % {"id": GA_ID}


PORTFOLIO_JS = open(os.path.join(TU, "portfolio.js"), encoding="utf-8").read()


def skripte(jez):
    t = T[jez]
    return GA + "<script>\n" + PORTFOLIO_JS + "</script>" + """<script>
const C={copy:%s,ok:%s};
document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>{
const el=document.getElementById(b.dataset.copy);
const ok=()=>{b.textContent=C.ok;setTimeout(()=>b.textContent=C.copy,1600)};
const sel=()=>{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r)};
try{navigator.clipboard.writeText(el.textContent).then(ok,sel)}catch(e){sel()}}));
</script><script>
(()=>{const c=document.getElementById("net");if(!c)return;const x=c.getContext("2d");let W=0,H,P=[],vid=true,radi=false;const R=matchMedia("(prefers-reduced-motion: reduce)").matches;
function size(){const r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);if(r.width===W&&P.length)return;W=r.width;H=r.height;c.width=W*d;c.height=H*d;x.setTransform(d,0,0,d,0,0);
const mali=W<600,n=Math.round(Math.min(mali?36:90,W*H/(mali?16000:14000)));P=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,r:Math.random()*1.4+.8}));draw()}
function draw(){x.clearRect(0,0,W,H);const D=W<600?120:150;
for(let i=0;i<P.length;i++){const a=P[i];for(let j=i+1;j<P.length;j++){const b=P[j],dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy);if(d<D){x.strokeStyle="rgba(120,170,255,"+(1-d/D)*.35+")";x.lineWidth=.8;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}}}
for(const p of P){x.fillStyle="rgba(170,215,255,.9)";x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fill()}}
function step(){if(!vid||document.hidden){radi=false;return}for(const p of P){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1}draw();requestAnimationFrame(step)}
function kreni(){if(!R&&!radi&&vid&&!document.hidden){radi=true;requestAnimationFrame(step)}}
addEventListener("resize",size);size();
if("IntersectionObserver"in window)new IntersectionObserver(e=>{vid=e[0].isIntersecting;kreni()}).observe(c);
document.addEventListener("visibilitychange",kreni);kreni()})();
</script>
</body>
</html>
""" % (json.dumps(t["c.copy"], ensure_ascii=False), json.dumps(t["c.ok"], ensure_ascii=False))


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
    podnozje = re.search(r"<footer>.*?</footer>", cela, re.S).group(0)
    telo404 = (f'{zaglavlje}\n<main id="top"><div class="hero"><canvas id="net" aria-hidden="true"></canvas>'
               f'<div class="w"><div class="eye">{n["eye"]}</div><h1>{n["h1"]}</h1>'
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
    return zaglavlje, re.search(r"<footer>.*?</footer>", cela, re.S).group(0)


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
