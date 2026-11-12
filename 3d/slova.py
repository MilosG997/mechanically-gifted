# Obrisi slova "MG" iz naslovnog fonta sajta (sajt/fonts/mg-serif.woff2) za 3D oznaku na zupčaniku.
# Pokretanje: python 3d/slova.py  ->  3d/src/mg-slova.json  (komande M/L/Q/Z, visina slova = 1)
import json
import os

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

TU = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(TU, "..", "sajt", "fonts", "mg-serif.woff2")


class Zapis(BasePen):
    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.k = []

    def _moveTo(self, p):
        self.k.append(["M", *p])

    def _lineTo(self, p):
        self.k.append(["L", *p])

    def _qCurveToOne(self, p1, p2):
        self.k.append(["Q", *p1, *p2])

    def _curveToOne(self, p1, p2, p3):
        self.k.append(["C", *p1, *p2, *p3])

    def _closePath(self):
        self.k.append(["Z"])


font = TTFont(FONT)
gs = font.getGlyphSet()
cmap = font.getBestCmap()
visina = font["OS/2"].sCapHeight
x, slova = 0, []
for znak in "MG":
    ime = cmap[ord(znak)]
    pen = Zapis(gs)
    gs[ime].draw(pen)
    pomeri = lambda v, i: (v + x if i % 2 == 0 else v)  # noqa: E731
    slova.append([[k[0], *[round(pomeri(v, i) / visina, 4) for i, v in enumerate(k[1:])]] for k in pen.k])
    x += gs[ime].width
json.dump({"sirina": round(x / visina, 4), "slova": slova}, open(os.path.join(TU, "src", "mg-slova.json"), "w"))
print("ok", round(x / visina, 3), [len(s) for s in slova])
