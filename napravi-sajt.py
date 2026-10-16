# Pravi sajt/ (SR i EN stranicu) iz dizajna mechanically-gifted-tech.html.
# Pokretanje: python napravi-sajt.py   (posle toga: napravi-slike.ps1 za PNG slike)
import html, json, os, re

DOMEN = "https://mechanicallygifted.rs"
EMAIL = "milosnpcz97@gmail.com"
TEL_PRIKAZ = "+381 69 3329 029"
TEL = "+381693329029"
LINKOVI = {
    "Eskay Products": "https://eskayproducts.com/",
    "Tan Ti Studio": "https://tantistudio.netlify.app/",
    "Majstori Pazova": "https://majstoripazova.rs/",
    "GitHub": "https://github.com/MilosG997",
    "QA": "https://github.com/MilosG997/qa-automation",
}
# Snimci projekata u sajt/img (pravi ih napravi-slike.py)
SLIKE = {"Eskay Products": "eskay", "Tan Ti Studio": "tanti", "Majstori Pazova": "majstori",
         "QA testovi i GitHub": "qa", "QA tests and GitHub": "qa"}

TU = os.path.dirname(os.path.abspath(__file__))
IZLAZ = os.path.join(TU, "sajt")
izvor = open(os.path.join(TU, "dizajn.html"), encoding="utf-8").read()

# Rečnik prevoda iz JS-a u fajlu
m = re.search(r"const T=\{en:(\{.*?\}),sr:(\{.*?\})\};", izvor, re.S)
T = {"en": json.loads(m.group(1)), "sr": json.loads(m.group(2))}

css = open(os.path.join(TU, "stil.css"), encoding="utf-8").read()

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

    # Portfolio linkovi u novom tabu
    for ime, url in LINKOVI.items():
        b = re.sub(r'(<div class="shot"[^>]*>' + re.escape(ime) + r'.*?)<a href="#">',
                   lambda mm: mm.group(1) + f'<a href="{url}" target="_blank" rel="noopener">', b, count=1, flags=re.S)
    # Poslednja kartica (QA testovi i GitHub) ima drugačiji naslov
    b = b.replace('<a href="#">', f'<a href="{LINKOVI["QA"]}" target="_blank" rel="noopener">', 1)
    assert 'href="#"' not in b

    # Prava slika projekta u kartici, naslov preko nje
    def snimak(mm):
        naslov = mm.group(1)
        ime = SLIKE[html.unescape(naslov)]
        return (f'<div class="shot"><img src="/img/{ime}.webp" alt="" width="960" height="540" '
                f'loading="lazy" decoding="async"><span>{naslov}</span></div>')
    b = re.sub(r'<div class="shot">([^<]*)</div>', snimak, b)

    # Podnožje: email, GitHub, drugi jezik
    drugi = ('<a href="/en/" hreflang="en" lang="en">English</a>' if jez == "sr"
             else '<a href="/" hreflang="sr" lang="sr">Srpski</a>')
    b = re.sub(r'<footer><div class="w"><span>(.*?)</span><span>(.*?)</span></div></footer>',
               lambda mm: f'<footer><div class="w"><span>{mm.group(1)} · {mm.group(2)}</span><nav>'
                          f'<a href="mailto:{EMAIL}">Email</a>'
                          f'<a href="{LINKOVI["GitHub"]}" target="_blank" rel="noopener">GitHub</a>'
                          f'{drugi}</nav></div></footer>', b, flags=re.S)
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
    return b


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


def glava(jez):
    k = META[jez]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": DOMEN + "/#firma", "name": "Mechanically Gifted",
         "url": k["url"], "description": k["usluga"], "email": EMAIL, "telephone": TEL,
         "logo": DOMEN + "/apple-touch-icon.png", "image": DOMEN + "/og-image.png",
         "address": {"@type": "PostalAddress", "addressCountry": "RS"},
         "areaServed": ["Srbija", "Europe"] if jez == "sr" else ["Serbia", "Europe"],
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
<meta name="description" content="{e(k["desc"])}">
<link rel="canonical" href="{k["url"]}">
<link rel="alternate" hreflang="sr" href="{DOMEN}/">
<link rel="alternate" hreflang="en" href="{DOMEN}/en/">
<link rel="alternate" hreflang="x-default" href="{DOMEN}/">
<meta name="theme-color" content="#050a1a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;650;700&family=Geist+Mono:wght@400;500;600&display=swap">
<style>{css}</style>
</head>
<body>
"""


def skripte(jez):
    t = T[jez]
    return """<script>
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

alt = (f'    <xhtml:link rel="alternate" hreflang="sr" href="{DOMEN}/"/>\n'
       f'    <xhtml:link rel="alternate" hreflang="en" href="{DOMEN}/en/"/>\n'
       f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMEN}/"/>\n')
with open(os.path.join(IZLAZ, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f'  <url>\n    <loc>{DOMEN}/</loc>\n{alt}  </url>\n'
            f'  <url>\n    <loc>{DOMEN}/en/</loc>\n{alt}  </url>\n'
            '</urlset>\n')

print("Gotovo:", IZLAZ)
