# Podaci za portfolio (SR i EN) + pravljenje slika za kartice i galeriju.
# Slike: python portfolio.py   (čita izvor-slika/figma i izvor-slika/snimci, piše sajt/img/portfolio)
import os

KATEGORIJE = [  # (ključ, SR, EN) — redosled filtera
    ("sve", "Sve", "All"), ("shopify", "Shopify", "Shopify"), ("sajtovi", "Sajtovi", "Websites"),
    ("dizajn", "Dizajn", "Design"), ("qa", "QA", "QA"),
]

# Redosled je i redosled u prikazu "Sve". izvor: lista (folder, fajl bez .png, isečak ili None)
RADOVI = [
    {"slug": "eskay", "kat": "shopify", "naslov": "Eskay Products", "chips": ["Shopify", "Klaviyo"],
     "link": "https://eskayproducts.com/", "alat": "Shopify · Klaviyo",
     "opis_kljuc": "w1.d",
     "alt": {"sr": "Početna stranica Shopify prodavnice Eskay Products", "en": "Eskay Products Shopify store home page"},
     "izvor": [("snimci", "eskay", None)]},
    {"slug": "majstori-pazova", "kat": "sajtovi", "naslov": "Majstori Pazova", "chips": [{"sr": "Aplikacija", "en": "App"}, "Android"],
     "link": "https://majstoripazova.rs/", "alat": "HTML · JavaScript · Firebase",
     "opis_kljuc": "w3.d",
     "alt": {"sr": "Početni ekran aplikacije Majstori Pazova sa kategorijama majstora",
             "en": "Majstori Pazova app home screen with tradesperson categories"},
     "izvor": [("snimci", "majstori", (300, 0, 680))]},
    {"slug": "qa-automation", "kat": "qa", "naslov": {"sr": "QA testovi i GitHub", "en": "QA tests and GitHub"},
     "chips": ["Selenium", "GitHub"], "link": "https://github.com/MilosG997/qa-automation",
     "link_tekst": {"sr": "Pogledaj QA testove na GitHub-u", "en": "View the QA tests on GitHub"},
     "alat": "Python · Selenium · pytest", "opis_kljuc": "w4.d",
     "alt": {"sr": "Terminal sa rezultatima Selenium testova koji su prošli",
             "en": "Terminal showing passing Selenium test results"},
     "izvor": [("snimci", "qa", None)]},
    # Tan Ti Studio: skinut dok sajt ne bude završen (vraća se odavde, slike ostaju u izvor-slika)
    # Dizajni iz Figme (freelance)
    {"slug": "shopnosis", "kat": "dizajn", "naslov": "Shopnosis",
     "opis": {"sr": "Landing stranica za platformu koja meri efekat reklama u prodavnicama.",
              "en": "Landing page for a platform that measures in-store media campaigns."},
     "alt": {"sr": "Dizajn sajta Shopnosis, svetloplava početna stranica sa video blokom",
             "en": "Shopnosis website design, light blue home page with a video block"},
     "izvor": [("figma", "1-37573", None)]},
    {"slug": "jr-technologies", "kat": "dizajn", "naslov": "JR Technologies",
     "opis": {"sr": "Sajt za tehnološku firmu koja pravi softver za turističke agencije.",
              "en": "Website for a tech company building software for travel agencies."},
     "alt": {"sr": "Dizajn sajta JR Technologies, tamna tema sa žutim akcentima",
             "en": "JR Technologies website design, dark theme with yellow accents"},
     "izvor": [("figma", "1-36962", None)]},
    {"slug": "gleam-dental", "kat": "dizajn", "naslov": "Gleam Dental",
     "opis": {"sr": "Sajt za stomatološku ordinaciju u dve verzije, sa uslugama i zakazivanjem pregleda.",
              "en": "Dental clinic website in two versions, with services and appointment booking."},
     "alt": {"sr": "Dizajn sajta stomatološke ordinacije Gleam", "en": "Gleam dental clinic website design"},
     "izvor": [("figma", "16-3743", None), ("figma", "16-3399", None)]},
    {"slug": "vermont", "kat": "dizajn", "naslov": "Vermont",
     "opis": {"sr": "Sajt za restoran: atmosfera, meni sa cenama i rezervacija stola.",
              "en": "Restaurant website: atmosphere, menu with prices and table booking."},
     "alt": {"sr": "Dizajn sajta restorana Vermont, tamna tema sa zlatnim detaljima",
             "en": "Vermont restaurant website design, dark theme with gold details"},
     "izvor": [("figma", "1-40774", None)]},
    {"slug": "infinity-task", "kat": "dizajn", "naslov": "Infinity Task",
     "opis": {"sr": "Landing stranica za aplikaciju za upravljanje zadacima tima.",
              "en": "Landing page for a team task management app."},
     "alt": {"sr": "Dizajn sajta Infinity Task, tamnoljubičasta tema sa prikazom aplikacije",
             "en": "Infinity Task website design, dark purple theme with app screenshots"},
     "izvor": [("figma", "1-40132", None)]},
    {"slug": "syne", "kat": "dizajn", "naslov": "Syne",
     "opis": {"sr": "Landing stranica za SaaS rešenja za firme, u tamnoj temi.",
              "en": "Landing page for enterprise SaaS solutions, in a dark theme."},
     "alt": {"sr": "Dizajn sajta Syne, tamna SaaS početna stranica", "en": "Syne website design, dark SaaS home page"},
     "izvor": [("figma", "15-256", None)]},
    {"slug": "urban-nest", "kat": "dizajn", "naslov": "Urban Nest",
     "opis": {"sr": "Sajt za planinski smeštaj: apartmani, galerija i rezervacija.",
              "en": "Mountain accommodation website: apartments, gallery and booking."},
     "alt": {"sr": "Dizajn sajta Urban Nest sa planinskim kućama pod snegom",
             "en": "Urban Nest website design with snowy mountain cabins"},
     "izvor": [("figma", "16-3105", None)]},
    {"slug": "dentissimo", "kat": "dizajn", "naslov": "Dentissimo",
     "opis": {"sr": "Sajt za stomatološku ordinaciju sa zakazivanjem posete.",
              "en": "Dental practice website with visit booking."},
     "alt": {"sr": "Dizajn sajta stomatološke ordinacije Dentissimo", "en": "Dentissimo dental practice website design"},
     "izvor": [("figma", "16-3989", None)]},
    {"slug": "temps", "kat": "dizajn", "naslov": "Temps",
     "opis": {"sr": "Sajt za NFT i digitalnu umetnost, tamna tema sa neon akcentima.",
              "en": "NFT and digital art website, dark theme with neon accents."},
     "alt": {"sr": "Dizajn sajta Temps za digitalnu umetnost", "en": "Temps digital art website design"},
     "izvor": [("figma", "1-40913", None)]},
    {"slug": "infinity-agency", "kat": "dizajn", "naslov": "Infinity Agency",
     "opis": {"sr": "Sajt za kreativnu agenciju sa menijem na dva jezika (EN/ESP).",
              "en": "Creative agency website with a two-language menu (EN/ESP)."},
     "alt": {"sr": "Dizajn sajta kreativne agencije Infinity", "en": "Infinity creative agency website design"},
     "izvor": [("figma", "1-39917", None)]},
    {"slug": "infinity-collab", "kat": "dizajn", "naslov": "Infinity Platform",
     "opis": {"sr": "Landing stranica za platformu za saradnju timova, od ideje do koda.",
              "en": "Landing page for a team collaboration platform, from concept to code."},
     "alt": {"sr": "Dizajn sajta Infinity platforme, ljubičasta tema", "en": "Infinity platform website design, purple theme"},
     "izvor": [("figma", "1-41045", None)]},
    {"slug": "infinity-analytics", "kat": "dizajn", "naslov": "Infinity Analytics",
     "opis": {"sr": "Landing stranica za alat za analizu proizvoda, sa ručno crtanim ilustracijama.",
              "en": "Landing page for a product analytics tool, with hand-drawn illustrations."},
     "alt": {"sr": "Dizajn sajta Infinity Analytics sa crno-belim ilustracijama",
             "en": "Infinity Analytics website design with black and white illustrations"},
     "izvor": [("figma", "1-37924", None)]},
]
for r in RADOVI:  # zajedničko za Figma dizajne
    if r["kat"] == "dizajn":
        r.setdefault("chips", ["Figma", {"sr": "Web dizajn", "en": "Web design"}])
        r.setdefault("alat", "Figma")
        r.setdefault("klijent", {"sr": "Freelance klijent", "en": "Freelance client"})


def jezik(v, jez):
    return v[jez] if isinstance(v, dict) else v


TU = os.path.dirname(os.path.abspath(__file__))
IZLAZ_IMG = os.path.join(TU, "sajt", "img", "portfolio")


def velicine():
    """Dimenzije gotovih slika (za width/height), bez ponovnog pravljenja."""
    from PIL import Image
    out = {}
    for r in RADOVI:
        out[r["slug"]] = [Image.open(os.path.join(IZLAZ_IMG, f'{r["slug"]}-{i + 1}.webp')).size
                          for i in range(len(r["izvor"]))]
    return out


if __name__ == "__main__":
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    os.makedirs(IZLAZ_IMG, exist_ok=True)
    for r in RADOVI:
        for i, (folder, ime, isecak) in enumerate(r["izvor"]):
            im = Image.open(os.path.join(TU, "izvor-slika", folder, ime + ".png")).convert("RGB")
            if isecak:
                x, y, w = isecak
                im = im.crop((x, y, x + w, y + round(w * 9 / 16)))
            # velika slika za galeriju: najviše 1800 px širine (dugačke stranice ostaju cele)
            if im.width > 1800:
                im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
            im.save(os.path.join(IZLAZ_IMG, f'{r["slug"]}-{i + 1}.webp'), "WEBP", quality=78, method=6)
            if i == 0:  # kartica: vrh slike u 16:9, 800 px
                vrh = im.crop((0, 0, im.width, min(im.height, round(im.width * 9 / 16))))
                vrh.resize((800, 450), Image.LANCZOS).save(
                    os.path.join(IZLAZ_IMG, f'{r["slug"]}-thumb.webp'), "WEBP", quality=80, method=6)
        print("ok", r["slug"])
