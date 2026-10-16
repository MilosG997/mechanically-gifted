# Pravi slike za sajt: og-image, apple-touch-icon i snimke projekata za portfolio.
# Pokretanje: python napravi-slike.py   (treba Chrome i: pip install pillow)
import os, subprocess, tempfile
from PIL import Image

TU = os.path.dirname(os.path.abspath(__file__))
SAJT = os.path.join(TU, "sajt")
IZVOR = os.path.join(TU, "izvor-slika")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFIL = os.path.join(tempfile.gettempdir(), "mg-chrome-profil")


def snimi(url, izlaz, w, h, cekaj=6000):
    os.makedirs(os.path.dirname(izlaz), exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    f"--user-data-dir={PROFIL}", (f"--virtual-time-budget={cekaj}" if url.startswith("file:") else f"--timeout={cekaj}"), f"--window-size={w},{h}",
                    f"--screenshot={izlaz}", url], timeout=60, capture_output=True)
    print(("ok  " if os.path.exists(izlaz) else "NEMA") + " " + izlaz)


def fajl(ime):
    return "file:///" + os.path.join(IZVOR, ime).replace("\\", "/")


snimi(fajl("og.html"), os.path.join(SAJT, "og-image.png"), 1200, 630)
snimi(fajl("ikonica.html"), os.path.join(SAJT, "apple-touch-icon.png"), 180, 180)

# Isečak (levo, gore, širina) — Tan Ti: bez prazne naslovne slike; Majstori: srednja kolona
ISECAK = {"tanti": (0, 0, 760), "majstori": (300, 0, 680)}
PROJEKTI = {
    "eskay": "https://eskayproducts.com/",
    "tanti": "https://tantistudio.netlify.app/",
    "majstori": "https://majstoripazova.rs/",
    "qa": fajl("qa.html"),
}
os.makedirs(os.path.join(SAJT, "img"), exist_ok=True)
for ime, url in PROJEKTI.items():
    png = os.path.join(IZVOR, "snimci", ime + ".png")
    try:
        snimi(url, png, 1280, 720, 12000)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", url)
    if os.path.exists(png):
        slika = Image.open(png).convert("RGB")
        if ime in ISECAK:
            x, y, w = ISECAK[ime]
            slika = slika.crop((x, y, x + w, y + round(w * 9 / 16)))
        slika.resize((960, 540), Image.LANCZOS).save(
            os.path.join(SAJT, "img", ime + ".webp"), "WEBP", quality=80, method=6)
