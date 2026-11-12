# Pravi fontove sajta iz izvornih varijabilnih fontova (OFL licenca, izvor-fontova/).
# Pokretanje: python napravi-fontove.py   (treba: pip install "fonttools[woff]")
#   mg-serif.woff2    Cormorant Garamond 500: naslovi, veliki brojevi, natpis u podnožju
#   mg-serif-i.woff2  Cormorant Garamond Italic 500: istaknute reči u naslovima
#   mg-sans.woff2     Archivo normalni (wdth 100), debljina 400–700: tekst
#   mg-mono.woff2     Martian Mono (wdth 100), debljina 450: oznake, terminal
# Svaki fajl ima samo latinicu, srpska slova (č ć đ š ž) i znake interpunkcije koje sajt koristi.
import os
import sys

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

sys.stdout.reconfigure(encoding="utf-8")
TU = os.path.dirname(os.path.abspath(__file__))
IZVOR = os.path.join(TU, "izvor-fontova")
IZLAZ = os.path.join(TU, "sajt", "fonts")

ZNACI = set(range(0x20, 0x7F)) | set(range(0xA0, 0x100))  # osnovna latinica i Latin-1
ZNACI |= {ord(c) for c in "ČčĆćĐđŠšŽž"}
ZNACI |= {0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022, 0x2026, 0x2032, 0x2033,
          0x20AC, 0x2122, 0x2190, 0x2191, 0x2192, 0x2193, 0x2197, 0x2212, 0x2713, 0x2715, 0x00D7}

FONTOVI = [
    ("mg-serif.woff2", "CormorantGaramond.ttf", {"wght": 500}),
    ("mg-serif-i.woff2", "CormorantGaramond-Italic.ttf", {"wght": 500}),
    ("mg-sans.woff2", "Archivo.ttf", {"wdth": 100, "wght": (400, 700)}),
    ("mg-mono.woff2", "MartianMono.ttf", {"wdth": 100, "wght": 450}),
]


def napravi(izlaz, izvor, ose):
    font = TTFont(os.path.join(IZVOR, izvor), lazy=False)
    if ose:  # varijabilni font: izdvoji širinu i debljinu koje sajt koristi
        font = instantiateVariableFont(font, ose)
    opcije = Options()
    opcije.flavor = "woff2"
    opcije.layout_features = ["kern", "liga", "calt", "case", "tnum", "lnum", "ss01"]
    opcije.desubroutinize = True
    opcije.hinting = False
    opcije.name_IDs = [0, 1, 2, 3, 4, 5, 6]
    s = Subsetter(opcije)
    postoje = set(font.getBestCmap())
    s.populate(unicodes=sorted(ZNACI & postoje))
    s.subset(font)
    font.flavor = "woff2"
    put = os.path.join(IZLAZ, izlaz)
    font.save(put)
    print(f"{izlaz:18} {os.path.getsize(put) / 1024:5.1f} KB  ({len(ZNACI & postoje)} znakova)")


if __name__ == "__main__":
    os.makedirs(IZLAZ, exist_ok=True)
    for args in FONTOVI:
        napravi(*args)
