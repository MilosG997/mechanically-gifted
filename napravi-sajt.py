# Pravi sajt/ (SR i EN stranicu) iz dizajna mechanically-gifted-tech.html.
# Pokretanje: python napravi-sajt.py   (posle toga: napravi-slike.ps1 za PNG slike)
import html, json, os, re

DOMEN = "https://mechanicallygifted.rs"
EMAIL = "mechanicallygifted@gmail.com"
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

# Fontovi (font-display: optional = bez kasnog treptanja/pomeranja teksta na sporoj mreži) su na našem serveru (sajt/fonts, OFL licenca) — brže od Google Fonts i keširaju se
LAT = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
       "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
LAT_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
           "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")
FONTOVI = "".join(
    f'@font-face{{font-family:"{ime}";font-style:normal;font-weight:100 900;font-display:optional;'
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

    # Recenzije sa Google-a iznad FAQ-a (podrazumevano mala traka; JS je zameni karticama kad ih ima)
    assert '<section id="pitanja">' in b
    b = b.replace('<section id="pitanja">', recenzije_html(jez) + '<section id="pitanja">', 1)

    # Portfolio: folderi iz portfolio.py
    assert "<!--PORTFOLIO-->" in b
    b = b.replace("<!--PORTFOLIO-->", portfolio_html(jez), 1)

    # Podnožje: email, GitHub, drugi jezik
    drugi = ('<a href="/en/" hreflang="en" lang="en">English</a>' if jez == "sr"
             else '<a href="/" hreflang="sr" lang="sr">Srpski</a>')
    b = re.sub(r'<footer><div class="w"><span>(.*?)</span><span>(.*?)</span></div></footer>',
               # bez zemlje na kraju; usluge su poseban deo koji na telefonu ide u svoj red (ceo)
               lambda mm: f'<footer><div class="w"><span class="ft"><span>{mm.group(1)}</span>'
                          f'<span class="ft-usl">{re.sub(r" · (Srbija|Serbia)$", "", mm.group(2))}</span></span><nav>'
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
    b = b.replace("</main>", "</main>\n" + galerija_json(jez), 1)
    return b


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
    return (f'{GOOGLE_G}<section id="recenzije" class="rev-sec rev-mala" data-tekst="{e(json.dumps(L, ensure_ascii=False))}">'
            f'<div class="w"><div class="rev-sum">'
            f'<div class="rev-poziv"><div class="rev-g"><svg width="24" height="24" aria-hidden="true"><use href="#revG"/></svg></div>'
            f'<span>{e(L["poziv"])}</span></div><div class="rev-acts">'
            f'<a class="btn btn-l rev-svi" href="{e(mape)}" target="_blank" rel="noopener" hidden>{e(L["svi"])}</a>'
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
            f'<div class="list">{"".join(stavke)}</div></div></div></div>')
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
<link rel="preload" href="/fonts/geist-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/geist-mono-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>{'<link rel="preload" href="/fonts/geist-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>' if jez == "sr" else ""}
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
const h=el.getAttribute("href")||"",stavka=el.closest(".folders .item");
if(h.startsWith("mailto:"))mgEvent("contact_email_click",{link_location:el.closest("footer")?"footer":"contact"});
else if(h.startsWith("tel:"))mgEvent("contact_phone_click");
else if(h.startsWith("viber:"))mgEvent("contact_viber_click");
else if(h.includes("wa.me/"))mgEvent("contact_whatsapp_click");
else if(el.dataset.copy)mgEvent("contact_copy_click",{field:el.dataset.copy==="v0"?"email":"phone"});
else if(el.matches(".ctas .btn-g")&&h.endsWith("#kontakt"))mgEvent("cta_free_quote_click");
else if(el.matches(".rev-ostavi"))mgEvent("review_leave_click",{link_location:el.closest(".rev-mala")?"strip":"reviews"});
else if(el.matches(".rev-svi"))mgEvent("review_see_all_click");
else if(stavka)mgEvent("portfolio_item_click",{item_name:stavka.querySelector("h3").textContent,link_url:el.href||""});
else if(el.hasAttribute("hreflang"))mgEvent("language_switch",{language_to:el.getAttribute("hreflang")})});
</script>
""" % {"id": GA_ID}


PORTFOLIO_JS = open(os.path.join(TU, "portfolio.js"), encoding="utf-8").read()
RECENZIJE_JS = open(os.path.join(TU, "recenzije.js"), encoding="utf-8").read()


def skripte(jez):
    t = T[jez]
    return GA + "<script>\n" + PORTFOLIO_JS + "</script><script>\n" + RECENZIJE_JS + "</script>" + """<script>
const C={copy:%s,ok:%s};
document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>{
const el=document.getElementById(b.dataset.copy);
const ok=()=>{b.textContent=C.ok;setTimeout(()=>b.textContent=C.copy,1600)};
const sel=()=>{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r)};
try{navigator.clipboard.writeText(el.textContent).then(ok,sel)}catch(e){sel()}}));
</script><script>
// Animirana mreža: u hederu (#net) i iza kontakt bloka (.mreza); svaka radi samo dok je na ekranu
document.querySelectorAll("#net, canvas.mreza").forEach(c=>{const x=c.getContext("2d");let W=0,H,P=[],vid=true,radi=false,spremno=false;const R=matchMedia("(prefers-reduced-motion: reduce)").matches;
function size(){const r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);if(r.width===W&&P.length)return;W=r.width;H=r.height;c.width=W*d;c.height=H*d;x.setTransform(d,0,0,d,0,0);
const mali=W<600,n=Math.round(Math.min(mali?36:90,W*H/(mali?16000:14000)));P=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,r:Math.random()*1.4+.8}));draw()}
function draw(){x.clearRect(0,0,W,H);const D=W<600?120:150;
for(let i=0;i<P.length;i++){const a=P[i];for(let j=i+1;j<P.length;j++){const b=P[j],dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy);if(d<D){x.strokeStyle="rgba(120,170,255,"+(1-d/D)*.35+")";x.lineWidth=.8;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}}}
for(const p of P){x.fillStyle="rgba(170,215,255,.9)";x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fill()}}
function step(){if(!vid||document.hidden){radi=false;return}for(const p of P){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1}draw();requestAnimationFrame(step)}
function kreni(){if(spremno&&!R&&!radi&&vid&&!document.hidden){radi=true;requestAnimationFrame(step)}}
addEventListener("resize",size);size();
if("IntersectionObserver"in window)new IntersectionObserver(e=>{vid=e[0].isIntersecting;kreni()}).observe(c);
document.addEventListener("visibilitychange",kreni);
// prvi kadar odmah (mirna mreža), pokret tek kad se stranica učita i procesor odmori — lakše učitavanje na telefonu
const pokreni=()=>{spremno=true;kreni()};const posle=()=>("requestIdleCallback"in window)?requestIdleCallback(pokreni,{timeout:2500}):setTimeout(pokreni,1200);
document.readyState==="complete"?posle():addEventListener("load",posle,{once:true})});
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
