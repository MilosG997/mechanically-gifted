// Pokreti na sajtu (ubacuje ih napravi-sajt.py u svaku stranicu). Sve poštuje "smanji pokrete" u sistemu.
(()=>{const d=document,R=matchMedia("(prefers-reduced-motion: reduce)").matches,mis=matchMedia("(hover:hover) and (pointer:fine)").matches;

// Pojavljivanje pri skrolu: [data-r] elementi, terminal (kuca redove), natpis u podnožju (puni se bojom)
const za=d.querySelectorAll("[data-r],.term,.ft-rec");
if("IntersectionObserver"in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}}),{rootMargin:"0px 0px -10% 0px",threshold:.12});za.forEach(el=>io.observe(el))}
else za.forEach(el=>el.classList.add("in"));

// Zaglavlje: traka napretka, sakrivanje pri skrolu nadole; koraci i velika traka prate skrol
const h=d.querySelector("header"),st=d.querySelector(".steps"),vel=[...d.querySelectorAll(".veliki-in")];
let py=scrollY,ceka=false;
function skrol(){ceka=false;const y=scrollY,dh=d.documentElement.scrollHeight-innerHeight;
if(h){h.style.setProperty("--sp",dh>0?(y/dh).toFixed(4):0);if(!h.classList.contains("otvoren"))h.classList.toggle("skriven",y>240&&y>py+2);if(y<py-2||y<240)h.classList.remove("skriven")}
py=y;
if(st){const r=st.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.62-r.top)/Math.max(1,r.height)));st.style.setProperty("--p",p.toFixed(3));
const k=st.children;for(let i=0;i<k.length;i++)k[i].classList.toggle("on",p>=i/k.length+.02)}
if(!R)for(const v of vel){const r=v.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)continue;const p=(innerHeight-r.top)/(innerHeight+r.height);v.style.transform="translate3d("+(-8-p*22).toFixed(2)+"%,0,0)"}}
addEventListener("scroll",()=>{if(!ceka){ceka=true;requestAnimationFrame(skrol)}},{passive:true});addEventListener("resize",skrol);skrol();

// Meni na telefonu
const mb=d.querySelector(".meni-btn");
if(mb&&h){const zatvori=()=>{h.classList.remove("otvoren");d.body.classList.remove("meni-otvoren");mb.setAttribute("aria-expanded","false")};
mb.addEventListener("click",()=>{const o=!h.classList.contains("otvoren");h.classList.toggle("otvoren",o);d.body.classList.toggle("meni-otvoren",o);mb.setAttribute("aria-expanded",o);if(o)h.classList.remove("skriven")});
d.querySelectorAll(".links a").forEach(a=>a.addEventListener("click",zatvori));
addEventListener("keydown",e=>{if(e.key==="Escape"&&h.classList.contains("otvoren")){zatvori();mb.focus()}});
addEventListener("resize",()=>{if(innerWidth>860)zatvori()})}

// Kartice: svetlo prati miš; dugmad: blago "magnetna"
d.querySelectorAll(".card").forEach(c=>c.addEventListener("pointermove",e=>{const r=c.getBoundingClientRect();c.style.setProperty("--mx",(e.clientX-r.left)+"px");c.style.setProperty("--my",(e.clientY-r.top)+"px")}));
if(mis&&!R){d.querySelectorAll(".btn-g,.btn-l").forEach(b=>{b.addEventListener("pointermove",e=>{const r=b.getBoundingClientRect();b.style.transform="translate("+((e.clientX-r.left-r.width/2)*.16).toFixed(1)+"px,"+((e.clientY-r.top-r.height/2)*.3).toFixed(1)+"px)"});b.addEventListener("pointerleave",()=>{b.style.transform=""})});
}

// QA sken oznaka u hederu (događaje šalje 3D)
const sk=d.querySelector(".sken");
if(sk)addEventListener("mg:sken",e=>{sk.classList.add("vidi");const p=e.detail.stanje==="prosao";sk.classList.toggle("prosao",p);sk.textContent=(p?sk.dataset.prosao:sk.dataset.radi).replace("{n}",String(e.detail.broj).padStart(2,"0"))});

// 3D u hederu: tek kad se stranica učita i korisnik se pomeri (ili posle 2,5 s), i samo ako pregledač ima WebGL
const sc=d.querySelector(".scena[data-js]");
if(sc){let krenuo=false;const dog=["pointermove","touchstart","scroll","keydown"];
const kreni=()=>{if(krenuo)return;krenuo=true;dog.forEach(t=>removeEventListener(t,kreni));
let gl=null;try{const p=d.createElement("canvas");gl=p.getContext("webgl2")||p.getContext("webgl")}catch(e){}
if(!gl)return;import(sc.dataset.js).then(m=>m.default(sc)).catch(()=>{})};
const posle=()=>{dog.forEach(t=>addEventListener(t,kreni,{passive:true}));setTimeout(kreni,2500)};
d.readyState==="complete"?posle():addEventListener("load",posle,{once:true})}
})();
