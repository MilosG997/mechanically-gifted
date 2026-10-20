# Podaci za portfolio "folderi" (SR i EN) + pravljenje slika.
# Slike: python portfolio.py   (čita izvor-slika/figma i izvor-slika/snimci, piše sajt/img/portfolio)
#   <slug>-thumb.webp  480x300 (16:10) za stavku u folderu
#   <slug>-N.webp      do 1800 px širine, za lightbox (samo Web dizajn)
import os

CLIENT = {"sr": "Freelance klijent", "en": "Freelance client"}
KONCEPT = {"sr": "Koncept", "en": "Concept"}


def figma(slug, naslov, opis, alt, izvori, oznaka=CLIENT):
    return {"slug": slug, "naslov": naslov, "opis": opis, "alt": alt, "oznaka": oznaka,
            "izvor": [("figma", i, None) for i in izvori], "lightbox": True}


FOLDERI = [
    {"key": "shopify", "naziv": {"sr": "Shopify", "en": "Shopify"},
     "opis": {"sr": "Web prodavnice, teme, merchandising i email marketing",
              "en": "Online stores, themes, merchandising and email marketing"},
     "stavke": [
         {"slug": "eskay", "naslov": "Eskay Products", "link": "https://eskayproducts.com/",
          "opis": {"sr": "Shopify tema, banneri za kolekcije, Klaviyo email kampanje i recenzije, blog i uvoz kataloga dobavljača.",
                   "en": "Shopify theme, collection banners, Klaviyo email campaigns and reviews, blog and supplier catalog import."},
          "alt": {"sr": "Početna stranica Shopify prodavnice Eskay Products", "en": "Eskay Products Shopify store home page"},
          "izvor": [("snimci", "eskay", None)]},
         {"slug": "hosiery-plus", "naslov": "Hosiery Plus", "link": "https://hosieryplus.com/",
          "opis": {"sr": "Merchandising prodavnice: praćenje stanja zaliha, sređivanje i organizacija kolekcija i proizvoda.",
                   "en": "Store merchandising: stock tracking, organizing collections and products."},
          "alt": {"sr": "Početna stranica Shopify prodavnice Hosiery Plus", "en": "Hosiery Plus Shopify store home page"},
          "izvor": [("snimci", "hosiery", None)]},
         {"slug": "tiptoe-boutique", "naslov": "Tiptoe Boutique", "link": "https://tiptoeboutique.com/",
          "opis": {"sr": "Merchandising prodavnice: praćenje stanja zaliha, sređivanje i organizacija kolekcija i proizvoda.",
                   "en": "Store merchandising: stock tracking, organizing collections and products."},
          "alt": {"sr": "Početna stranica Shopify prodavnice Tiptoe Boutique", "en": "Tiptoe Boutique Shopify store home page"},
          "izvor": [("snimci", "tiptoe", None)]},
     ]},
    {"key": "sajtovi", "naziv": {"sr": "Sajtovi i aplikacije", "en": "Websites & apps"},
     "opis": {"sr": "Live sajtovi i aplikacije", "en": "Live websites and apps"},
     "stavke": [
         {"slug": "majstori-pazova", "naslov": "Majstori Pazova", "link": "https://majstoripazova.rs/",
          "opis": {"sr": "Web i Android aplikacija sa majstorima po kategorijama, ocenama i direktnim pozivom.",
                   "en": "Web and Android app listing tradespeople by category, with ratings and direct calling."},
          "alt": {"sr": "Početni ekran aplikacije Majstori Pazova sa kategorijama majstora",
                  "en": "Majstori Pazova app home screen with tradesperson categories"},
          "izvor": [("snimci", "majstori", (300, 0, 680))]},
     ]},
    {"key": "dizajn", "naziv": {"sr": "Web dizajn", "en": "Web design"},
     "opis": {"sr": "Dizajni u Figmi", "en": "Figma designs"},
     "stavke": [
         figma("shopnosis", "Shopnosis",
               {"sr": "Landing stranica za platformu koja meri efekat reklama u prodavnicama.",
                "en": "Landing page for a platform that measures in-store media campaigns."},
               {"sr": "Web dizajn Shopnosis, svetloplava početna stranica sa video blokom",
                "en": "Shopnosis web design, light blue home page with a video block"}, ["1-37573"]),
         figma("jr-technologies", "JR Technologies",
               {"sr": "Sajt za tehnološku firmu koja pravi softver za turističke agencije.",
                "en": "Website for a tech company building software for travel agencies."},
               {"sr": "Web dizajn JR Technologies, tamna tema sa žutim akcentima",
                "en": "JR Technologies web design, dark theme with yellow accents"}, ["1-36962"]),
         figma("gleam-dental", "Gleam Dental",
               {"sr": "Sajt za stomatološku ordinaciju u dve verzije, sa uslugama i zakazivanjem pregleda.",
                "en": "Dental clinic website in two versions, with services and appointment booking."},
               {"sr": "Web dizajn stomatološke ordinacije Gleam", "en": "Gleam dental clinic web design"},
               ["16-3743", "16-3399"]),
         figma("vermont", "Vermont",
               {"sr": "Sajt za restoran: atmosfera, meni sa cenama i rezervacija stola.",
                "en": "Restaurant website: atmosphere, menu with prices and table booking."},
               {"sr": "Web dizajn restorana Vermont, tamna tema sa zlatnim detaljima",
                "en": "Vermont restaurant web design, dark theme with gold details"}, ["1-40774"]),
         figma("syne", "Syne",
               {"sr": "Landing stranica za SaaS rešenja za firme, u tamnoj temi.",
                "en": "Landing page for enterprise SaaS solutions, in a dark theme."},
               {"sr": "Web dizajn Syne, tamna SaaS početna stranica", "en": "Syne web design, dark SaaS home page"},
               ["15-256"]),
         figma("urban-nest", "Urban Nest",
               {"sr": "Sajt za planinski smeštaj: apartmani, galerija i rezervacija.",
                "en": "Mountain accommodation website: apartments, gallery and booking."},
               {"sr": "Web dizajn Urban Nest sa planinskim kućama pod snegom",
                "en": "Urban Nest web design with snowy mountain cabins"}, ["16-3105"]),
         figma("dentissimo", "Dentissimo",
               {"sr": "Sajt za stomatološku ordinaciju sa zakazivanjem posete.",
                "en": "Dental practice website with visit booking."},
               {"sr": "Web dizajn stomatološke ordinacije Dentissimo", "en": "Dentissimo dental practice web design"},
               ["16-3989"]),
         figma("temps", "Temps",
               {"sr": "Sajt za NFT i digitalnu umetnost, tamna tema sa neon akcentima.",
                "en": "NFT and digital art website, dark theme with neon accents."},
               {"sr": "Web dizajn Temps za digitalnu umetnost", "en": "Temps digital art web design"}, ["1-40913"]),
         figma("infinity-serija", {"sr": "Infinity serija – 4 landing stranice", "en": "Infinity series – 4 landing pages"},
               {"sr": "Četiri SaaS landing stranice: saradnja timova, upravljanje zadacima, kreativna agencija i analiza proizvoda.",
                "en": "Four SaaS landing pages: team collaboration, task management, a creative agency and product analytics."},
               {"sr": "Web dizajn Infinity serije, četiri landing stranice", "en": "Infinity series web design, four landing pages"},
               ["1-41045", "1-40132", "1-39917", "1-37924"], oznaka=KONCEPT),
     ]},
    {"key": "qa", "naziv": {"sr": "QA testiranje", "en": "QA testing"},
     "opis": {"sr": "Automatski testovi", "en": "Automated tests"},
     "stavke": [
         {"slug": "qa-automation", "naslov": {"sr": "QA testovi i GitHub", "en": "QA tests and GitHub"},
          "link": "https://github.com/MilosG997/qa-automation",
          "link_tekst": {"sr": "Pogledaj na GitHub-u", "en": "View on GitHub"},
          "opis": {"sr": "Selenium i pytest testovi za Shopify prodavnicu i moje sajtove, sa automatskim pokretanjem na GitHub-u.",
                   "en": "Selenium and pytest tests for a Shopify store and my websites, running automatically on GitHub."},
          "alt": {"sr": "Terminal sa rezultatima Selenium testova koji su prošli",
                  "en": "Terminal showing passing Selenium test results"},
          "izvor": [("snimci", "qa", None)]},
     ]},
]


def jezik(v, jez):
    return v[jez] if isinstance(v, dict) else v


TU = os.path.dirname(os.path.abspath(__file__))
IZLAZ_IMG = os.path.join(TU, "sajt", "img", "portfolio")
THUMB = (480, 300)


def stavke():
    for f in FOLDERI:
        yield from f["stavke"]


def velicine():
    """Dimenzije velikih slika (za width/height u lightbox-u), bez ponovnog pravljenja."""
    from PIL import Image
    return {s["slug"]: [Image.open(os.path.join(IZLAZ_IMG, f'{s["slug"]}-{i + 1}.webp')).size
                        for i in range(len(s["izvor"]))]
            for s in stavke() if s.get("lightbox")}


if __name__ == "__main__":
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    os.makedirs(IZLAZ_IMG, exist_ok=True)
    potrebni = set()
    for s in stavke():
        for i, (folder, ime, isecak) in enumerate(s["izvor"]):
            im = Image.open(os.path.join(TU, "izvor-slika", folder, ime + ".png")).convert("RGB")
            if isecak:
                x, y, w = isecak
                im = im.crop((x, y, x + w, y + round(w * 9 / 16)))
            if s.get("lightbox"):  # velika slika za galeriju: najviše 1800 px širine
                if im.width > 1800:
                    im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
                ime_velike = f'{s["slug"]}-{i + 1}.webp'
                im.save(os.path.join(IZLAZ_IMG, ime_velike), "WEBP", quality=78, method=6)
                potrebni.add(ime_velike)
            if i == 0:  # stavka u folderu: vrh slike u 16:10
                h = min(im.height, round(im.width * 10 / 16))
                vrh = im.crop((0, 0, round(h * 16 / 10), h)) if h < round(im.width * 10 / 16) else im.crop((0, 0, im.width, h))
                vrh.resize(THUMB, Image.LANCZOS).save(os.path.join(IZLAZ_IMG, f'{s["slug"]}-thumb.webp'),
                                                      "WEBP", quality=80, method=6)
                potrebni.add(f'{s["slug"]}-thumb.webp')
        print("ok", s["slug"])
    for f in os.listdir(IZLAZ_IMG):  # stare slike koje više ne koristimo
        if f not in potrebni:
            os.remove(os.path.join(IZLAZ_IMG, f))
            print("obrisano", f)
