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
# Ikonice iz jednog snimka 512x512: Apple (180), manifest (192, 512) i favicon.ico (16/32/48)
ikona = os.path.join(IZVOR, "snimci", "ikonica-512.png")
snimi(fajl("ikonica.html"), ikona, 512, 512)
velika = Image.open(ikona).convert("RGB")
for ime, v in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
    velika.resize((v, v), Image.LANCZOS).save(os.path.join(SAJT, ime), optimize=True)
# favicon.ico ima zaobljene uglove kao favicon.svg
from PIL import ImageDraw
maska = Image.new("L", (512, 512), 0)
ImageDraw.Draw(maska).rounded_rectangle((0, 0, 511, 511), radius=128, fill=255)
zaobljena = velika.convert("RGBA")
zaobljena.putalpha(maska)
zaobljena.save(os.path.join(SAJT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# Isečak (levo, gore, širina) — Tan Ti: bez prazne naslovne slike; Majstori: srednja kolona
ISECAK = {"tanti": (0, 0, 760), "majstori": (300, 0, 680)}
PROJEKTI = {
    "eskay": "https://eskayproducts.com/",
    "tanti": "https://tantistudio.netlify.app/",
    "majstori": "https://majstoripazova.rs/",
    "qa": fajl("qa.html"),
}
for ime, url in PROJEKTI.items():
    png = os.path.join(IZVOR, "snimci", ime + ".png")
    try:
        snimi(url, png, 1280, 720, 12000)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", url)
# snimci (izvor-slika/snimci/*.png) dalje obrađuje portfolio.py
