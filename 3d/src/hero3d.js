// 3D u hederu: sklop zupčanika sa MG oznakom. Prvo se iscrta kao plavi nacrt, pa se "izlije" u metal i pokrene;
// prati miš i skrol, a povremeno ga pređe plavi QA sken (događaj "mg:sken" za oznaku u HTML-u).
// Učitava se tek posle stranice (vidi napravi-sajt.py), radi samo dok je heder na ekranu.
import {
  AdditiveBlending, CanvasTexture, Color, CylinderGeometry, DirectionalLight, DoubleSide, EdgesGeometry,
  ExtrudeGeometry, Group, InstancedMesh, LineBasicMaterial, LineSegments, Matrix4, Mesh, MeshBasicMaterial,
  MeshStandardMaterial, NeutralToneMapping, Path, PerspectiveCamera, PlaneGeometry, PMREMGenerator, PointLight,
  Scene, Shape, SRGBColorSpace, TorusGeometry, BoxGeometry, WebGLRenderer,
} from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import slova from "./mg-slova.json";

const TAU = Math.PI * 2;
const m = 0.16; // modul zupčanika (veličina zuba)

function polar(r, a) {
  return [Math.cos(a) * r, Math.sin(a) * r];
}

// Obris zupčanika: n zuba, zub 0 centriran na uglu 0; prohodi = sektori (krakovi) ili okrugle rupe
function oblikZupcanika(n, { sektori = 0, rupe = 0, osovina = 0.18 } = {}) {
  const rp = (m * n) / 2, ra = rp + m, rf = rp - 1.25 * m, k = TAU / n;
  const s = new Shape();
  for (let i = 0; i < n; i++) {
    const a = i * k;
    const p0 = polar(rf, a - k * 0.27), c0 = polar(rp, a - k * 0.25), p1 = polar(ra, a - k * 0.13);
    const p2 = polar(ra, a + k * 0.13), c1 = polar(rp, a + k * 0.25), p3 = polar(rf, a + k * 0.27);
    if (i === 0) s.moveTo(...p0); else s.lineTo(...p0);
    s.quadraticCurveTo(...c0, ...p1);
    s.lineTo(...p2);
    s.quadraticCurveTo(...c1, ...p3);
  }
  s.closePath();
  if (sektori) {
    const r1 = rp * 0.42, r2 = rf - rp * 0.16, sirina = TAU / sektori, krak = 0.24 / rp;
    for (let i = 0; i < sektori; i++) {
      const a0 = i * sirina + krak, a1 = (i + 1) * sirina - krak;
      const h = new Path();
      h.moveTo(...polar(r2, a0));
      h.absarc(0, 0, r2, a0, a1, false);
      h.lineTo(...polar(r1, a1));
      h.absarc(0, 0, r1, a1, a0, true);
      h.closePath();
      s.holes.push(h);
    }
  }
  if (rupe) {
    const rr = rp * 0.55, vel = rp * 0.17;
    for (let i = 0; i < rupe; i++) {
      const [x, y] = polar(rr, (i / rupe) * TAU + k / 2);
      const h = new Path();
      h.absarc(x, y, vel, 0, TAU, true);
      s.holes.push(h);
    }
  }
  const h = new Path();
  h.absarc(0, 0, osovina, 0, TAU, true);
  s.holes.push(h);
  return { s, rp, ra };
}

function geometrija(shape, dubina, kosina = 0.05) {
  const g = new ExtrudeGeometry(shape, {
    depth: dubina, bevelEnabled: true, bevelThickness: kosina, bevelSize: kosina * 0.8, bevelSegments: 2, curveSegments: 10,
  });
  g.translate(0, 0, -dubina / 2);
  g.computeVertexNormals();
  return g;
}

// "MG" iz naslovnog fonta sajta (3d/slova.py), centrirano, visina h
function oblikSlova(h) {
  const s = h, ox = (-slova.sirina * h) / 2, oy = -h / 2, likovi = [];
  for (const slovo of slova.slova) {
    let sh = null;
    for (const [c, ...v] of slovo) {
      const p = (i) => [v[i] * s + ox, v[i + 1] * s + oy];
      if (c === "M") { sh = new Shape(); sh.moveTo(...p(0)); likovi.push(sh); }
      else if (c === "L") sh.lineTo(...p(0));
      else if (c === "Q") sh.quadraticCurveTo(...p(0), ...p(2));
      else if (c === "C") sh.bezierCurveTo(...p(0), ...p(2), ...p(4));
    }
  }
  return likovi;
}

function gradijent() {
  const c = document.createElement("canvas");
  c.width = 4; c.height = 128;
  const x = c.getContext("2d"), g = x.createLinearGradient(0, 0, 0, 128);
  g.addColorStop(0, "rgba(89,195,255,0)");
  g.addColorStop(0.5, "rgba(89,195,255,1)");
  g.addColorStop(1, "rgba(89,195,255,0)");
  x.fillStyle = g;
  x.fillRect(0, 0, 4, 128);
  return new CanvasTexture(c);
}

const lagano = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));

export default function pokreni(kontejner) {
  const mirno = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const platno = document.createElement("canvas");
  platno.setAttribute("aria-hidden", "true");
  let renderer;
  try {
    renderer = new WebGLRenderer({ canvas: platno, antialias: true, alpha: true, powerPreference: "high-performance" });
  } catch (e) {
    return;
  }
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = NeutralToneMapping;
  renderer.toneMappingExposure = 0.95;
  kontejner.appendChild(platno);

  const scena = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  scena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();
  scena.environmentIntensity = 0.28;

  const kamera = new PerspectiveCamera(30, 1, 0.1, 100);
  kamera.position.set(0, 0, 17);

  const svetlo = new DirectionalLight(0xdfe8ff, 1.0);
  svetlo.position.set(-6, 7, 9);
  scena.add(svetlo);
  const plava = new PointLight(0x2f5bff, 38, 40, 1.6);
  plava.position.set(5, -3, -2.5);
  scena.add(plava);
  const nebo = new PointLight(0x59c3ff, 12, 40, 1.6);
  nebo.position.set(-6, -5, 5);
  scena.add(nebo);

  const tamni = new MeshStandardMaterial({ color: 0x10162a, metalness: 1, roughness: 0.4 });
  const hrom = new MeshStandardMaterial({ color: 0x6c789a, metalness: 1, roughness: 0.26 });
  const plavi = new MeshStandardMaterial({ color: 0x2f5bff, metalness: 0.5, roughness: 0.3, emissive: 0x2450ff, emissiveIntensity: 0.9 });
  const sjaj = new MeshStandardMaterial({ color: 0xe9f1ff, metalness: 0.2, roughness: 0.25, emissive: 0x59c3ff, emissiveIntensity: 1.6 });

  // Zupčanici: centar, broj zuba, ugao u odnosu na prethodni (sa kojim se zahvata), materijal
  const sklop = new Group();
  const zupcanici = [];
  function dodaj(n, opts, mat, dubina, roditelj, ugao) {
    const { s, rp, ra } = oblikZupcanika(n, opts);
    const geo = geometrija(s, dubina);
    const mesh = new Mesh(geo, mat.clone());
    let x = 0, y = 0, faza = 0, w = 0;
    if (roditelj) {
      const d = roditelj.rp + rp;
      [x, y] = [roditelj.x + Math.cos(ugao) * d, roditelj.y + Math.sin(ugao) * d];
      // Faza: kad je zub roditelja tačno na pravcu dodira, ovde je procep (pravac ugao+π). Roditelj okrenut
      // za Δ u smeru kazaljke unazad pomera procep ovog zupčanika za -Δ·n1/n, pa je početna faza:
      faza = ugao + Math.PI - Math.PI / n + ((ugao - roditelj.faza) * roditelj.n) / n;
      w = (-roditelj.w * roditelj.n) / n;
    } else {
      w = 1;
    }
    mesh.position.set(x, y, 0);
    mesh.material.userData.osnova = mesh.material.emissive.clone();
    const z = { n, rp, ra, x, y, faza, w, mesh, linije: null, tezina: 0 };
    const ivice = new LineSegments(new EdgesGeometry(geo, 24), new LineBasicMaterial({
      color: 0x7fd3ff, transparent: true, opacity: 0.95, blending: AdditiveBlending, depthWrite: false,
    }));
    mesh.add(ivice);
    z.linije = ivice;
    z.ukupno = ivice.geometry.attributes.position.count;
    sklop.add(mesh);
    zupcanici.push(z);
    return z;
  }

  const g1 = dodaj(30, { sektori: 6, osovina: 0.32 }, tamni, 0.62, null);
  const g2 = dodaj(14, { rupe: 4, osovina: 0.16 }, hrom, 0.54, g1, -0.36);
  const g3 = dodaj(20, { rupe: 5, osovina: 0.2 }, tamni, 0.54, g1, 2.42);
  const g4 = dodaj(10, { osovina: 0.12 }, plavi, 0.5, g2, -1.62);

  // Glavčina velikog zupčanika sa MG oznakom
  const glavcina = new Mesh(new CylinderGeometry(1.06, 1.06, 0.86, 64), tamni.clone());
  glavcina.rotation.x = Math.PI / 2;
  g1.mesh.add(glavcina);
  const prsten = new Mesh(new TorusGeometry(1.06, 0.045, 12, 96), sjaj);
  prsten.position.z = 0.44;
  g1.mesh.add(prsten);
  const oznaka = new Mesh(geometrija(oblikSlova(0.6), 0.14, 0.025), plavi.clone());
  oznaka.position.z = 0.5;
  sklop.add(oznaka); // ne okreće se sa zupčanikom: MG uvek stoji uspravno

  // Brojčanik iza: tanak prsten sa crticama
  const brojcanik = new Group();
  const okvir = new Mesh(new TorusGeometry(3.25, 0.018, 8, 160), new MeshBasicMaterial({ color: 0x3a5bd6, transparent: true, opacity: 0.55 }));
  brojcanik.add(okvir);
  const crtice = new InstancedMesh(new BoxGeometry(0.02, 0.16, 0.02), new MeshBasicMaterial({ color: 0x59c3ff, transparent: true, opacity: 0.5 }), 72);
  const mx = new Matrix4();
  for (let i = 0; i < 72; i++) {
    const a = (i / 72) * TAU, duga = i % 6 === 0;
    mx.makeRotationZ(a - Math.PI / 2).setPosition(Math.cos(a) * 3.42, Math.sin(a) * 3.42, 0);
    if (duga) mx.scale({ x: 1.6, y: 1.8, z: 1 });
    crtice.setMatrixAt(i, mx);
  }
  brojcanik.add(crtice);
  brojcanik.position.z = -0.75;
  sklop.add(brojcanik);

  // QA sken: tanka linija i blagi sjaj koji pređu preko sklopa
  const sken = new Group();
  const linija = new Mesh(new PlaneGeometry(10.5, 0.03), new MeshBasicMaterial({ color: 0xbfeaff, transparent: true, opacity: 0, blending: AdditiveBlending, depthWrite: false, side: DoubleSide }));
  const oreol = new Mesh(new PlaneGeometry(10.5, 1.1), new MeshBasicMaterial({ map: gradijent(), transparent: true, opacity: 0, blending: AdditiveBlending, depthWrite: false, side: DoubleSide }));
  sken.add(linija, oreol);
  sken.position.z = 0.75;
  sklop.add(sken);

  // Centriranje sklopa
  const sredina = { x: (g3.x - g3.ra + Math.max(g2.x + g2.ra, g4.x + g4.ra)) / 2, y: (g4.y - g4.ra + g3.y + g3.ra) / 2 };
  sklop.children.forEach((c) => { c.position.x -= sredina.x; c.position.y -= sredina.y; });
  zupcanici.forEach((z) => { z.cy = z.y - sredina.y; });
  const svet = new Group();
  svet.add(sklop);
  scena.add(svet);

  // Raspored po veličini ekrana
  let sirina = 1, visina = 1, raspored = { x: 0, y: 0, s: 1 };
  function rasporedi() {
    const r = kontejner.getBoundingClientRect();
    sirina = Math.max(1, r.width); visina = Math.max(1, r.height);
    const dpr = Math.min(devicePixelRatio || 1, sirina < 700 ? 1.5 : 1.75);
    renderer.setPixelRatio(dpr);
    renderer.setSize(sirina, visina, false);
    kamera.aspect = sirina / visina;
    kamera.updateProjectionMatrix();
    const vh = 2 * kamera.position.z * Math.tan((kamera.fov * Math.PI) / 360), vw = vh * kamera.aspect;
    if (kamera.aspect >= 1.25) raspored = { x: vw * 0.235, y: -vh * 0.03, s: Math.min((vw * 0.42) / 9.4, (vh * 0.74) / 9.2) };
    else if (kamera.aspect >= 0.85) raspored = { x: vw * 0.2, y: -vh * 0.12, s: (vh * 0.62) / 9.2 };
    else {  // telefon: sklop ispod dugmadi, poravnat na dno hedera (CSS mu ostavlja prostor)
      const s = Math.min((vw * 0.9) / 9.4, (vh * 0.42) / 9.2);
      raspored = { x: vw * 0.16, y: -vh / 2 + 4.3 * s, s };
    }
  }
  rasporedi();
  new ResizeObserver(() => { rasporedi(); if (!radi) crtaj(performance.now()); }).observe(kontejner);

  // Miš i skrol
  let mxc = 0, myc = 0, ciljX = 0, ciljY = 0;
  addEventListener("pointermove", (e) => {
    ciljX = (e.clientX / innerWidth) * 2 - 1;
    ciljY = (e.clientY / innerHeight) * 2 - 1;
  }, { passive: true });
  const heder = kontejner.closest(".hero") || kontejner;

  // Sken
  const PERIOD = 6.5, TRAJE = 1.9;
  let poslednjiSken = -1, brojSkena = 0;
  const javi = (stanje) => dispatchEvent(new CustomEvent("mg:sken", { detail: { stanje, broj: brojSkena } }));

  const pocetak = performance.now();
  let ugao = 0, preth = pocetak, radi = false;
  const bojaSken = new Color(0x59c3ff);

  function crtaj(sad) {
    const t = (sad - pocetak) / 1000, dt = Math.min(0.05, (sad - preth) / 1000);
    preth = sad;
    const p = Math.min(1, Math.max(0, scrollY / Math.max(1, heder.offsetHeight)));

    // Uvod: nacrt (linije) -> metal
    zupcanici.forEach((z, i) => {
      const crtanje = mirno ? 1 : lagano((t - 0.1 - i * 0.18) / 1.25);
      z.linije.geometry.setDrawRange(0, Math.floor(z.ukupno * crtanje / 2) * 2);
      const metal = mirno ? 1 : lagano((t - 1.1 - i * 0.12) / 0.9);
      z.mesh.material.opacity = metal;
      z.mesh.material.transparent = metal < 1;
      z.linije.material.opacity = mirno ? 0.08 : 0.95 - 0.87 * lagano((t - 1.7 - i * 0.12) / 0.9);
    });
    const ostalo = mirno ? 1 : lagano((t - 1.4) / 0.8);
    [glavcina, prsten, oznaka].forEach((o) => { o.material.transparent = ostalo < 1; o.material.opacity = ostalo; });
    okvir.material.opacity = 0.55 * ostalo; crtice.material.opacity = 0.5 * ostalo;

    // Okretanje: pravilni odnosi zuba, brže dok se skroluje
    const brzina = mirno ? 0 : lagano((t - 1.6) / 1.6) * (1 + p * 4);
    ugao += dt * brzina;
    zupcanici.forEach((z) => { z.mesh.rotation.z = z.faza + ugao * z.w * 0.32; });
    brojcanik.rotation.z = -ugao * 0.08;

    // Miš (glatko), skrol (sklop odlazi gore i okreće se)
    mxc += (ciljX - mxc) * 0.05; myc += (ciljY - myc) * 0.05;
    svet.position.set(raspored.x, raspored.y + p * (kamera.aspect < 0.85 ? 1.2 : 3.2), 0);
    svet.scale.setScalar(raspored.s * (1 - p * 0.18));
    sklop.rotation.set(-0.38 + myc * 0.22 + p * 0.5, -0.5 + mxc * 0.32, p * 0.7);

    // QA sken na svakih PERIOD sekundi
    zupcanici.forEach((z) => { z.tezina = Math.max(0, z.tezina - dt * 1.6); });
    if (!mirno && t > 3.2) {
      const tt = (t - 3.2) % PERIOD, ciklus = Math.floor((t - 3.2) / PERIOD);
      if (ciklus !== poslednjiSken && tt < TRAJE) { poslednjiSken = ciklus; brojSkena++; javi("radi"); }
      if (tt < TRAJE) {
        const f = tt / TRAJE, y = 4.9 - f * 9.8;
        sken.position.y = y;
        const vid = Math.sin(Math.PI * f);
        linija.material.opacity = 0.95 * vid;
        oreol.material.opacity = 0.35 * vid;
        zupcanici.forEach((z) => { if (Math.abs(z.cy - y) < z.ra * 0.9) z.tezina = Math.min(1, z.tezina + dt * 5); });
        if (tt + dt >= TRAJE) javi("prosao");
      } else {
        linija.material.opacity = 0;
        oreol.material.opacity = 0;
      }
    }
    zupcanici.forEach((z) => {
      const mat = z.mesh.material;
      mat.emissive.copy(mat.userData.osnova).lerp(bojaSken, z.tezina * 0.6);
    });

    renderer.render(scena, kamera);
  }

  function petlja(sad) { crtaj(sad); }
  let vidljiv = true;
  function osvezi() {
    const treba = vidljiv && !document.hidden && !mirno;
    if (treba && !radi) { radi = true; preth = performance.now(); renderer.setAnimationLoop(petlja); }
    else if (!treba && radi) { radi = false; renderer.setAnimationLoop(null); }
  }
  new IntersectionObserver((e) => { vidljiv = e[0].isIntersecting; osvezi(); }).observe(kontejner);
  document.addEventListener("visibilitychange", osvezi);
  if (mirno) addEventListener("scroll", () => crtaj(performance.now()), { passive: true });
  crtaj(performance.now());
  osvezi();
  kontejner.classList.add("spremno");
  return () => { renderer.setAnimationLoop(null); renderer.dispose(); };
}
