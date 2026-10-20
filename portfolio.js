// Portfolio "folderi": jedan otvoren u isto vreme; lightbox za Web dizajn (strelice, Esc, klik van slike, swipe).
(()=>{const folderi=[...document.querySelectorAll(".folders .f")];if(!folderi.length)return;
function postavi(f,otvoren){f.classList.toggle("open",otvoren);f.querySelector(".head").setAttribute("aria-expanded",otvoren);
const telo=f.querySelector(".body");otvoren?telo.removeAttribute("inert"):telo.setAttribute("inert","")}
folderi.forEach(f=>f.querySelector(".head").addEventListener("click",()=>{
const otvori=!f.classList.contains("open");folderi.forEach(o=>postavi(o,false));
if(otvori){postavi(f,true);window.mgEvent&&mgEvent("portfolio_folder_open",{folder_name:f.querySelector(".t b").textContent})}}));

// Lightbox: prozor se pravi tek pri prvom otvaranju (nema skrivenog teksta u stranici)
const podaci=document.getElementById("galerija");if(!podaci)return;
const G=JSON.parse(podaci.textContent),T=G.tekst;let lb,slike,naslov,opis,meta,broj,tren=0,pre=null;
function napravi(){lb=document.createElement("div");lb.className="lb";lb.id="lb";lb.hidden=true;
lb.setAttribute("role","dialog");lb.setAttribute("aria-modal","true");lb.setAttribute("aria-labelledby","lbNaslov");
lb.innerHTML=`<button type="button" class="lb-x" aria-label="${T.zatvori}">&times;</button>`+
`<button type="button" class="lb-nav lb-pre" aria-label="${T.pre}">&#8249;</button>`+
`<button type="button" class="lb-nav lb-sled" aria-label="${T.sled}">&#8250;</button>`+
`<div class="lb-okvir"><div class="lb-slike"></div><div class="lb-info"><div><h3 id="lbNaslov"></h3><p></p></div>`+
`<div class="lb-meta"><span class="lb-alat"></span><span class="lb-broj"></span></div></div></div>`;
document.body.appendChild(lb);slike=lb.querySelector(".lb-slike");naslov=lb.querySelector("h3");opis=lb.querySelector(".lb-info p");
meta=lb.querySelector(".lb-alat");broj=lb.querySelector(".lb-broj");
lb.querySelector(".lb-x").addEventListener("click",zatvori);
lb.querySelector(".lb-pre").addEventListener("click",()=>korak(-1));
lb.querySelector(".lb-sled").addEventListener("click",()=>korak(1));
lb.addEventListener("click",e=>{if(e.target===lb)zatvori()});
let x0=null,y0=0;lb.addEventListener("touchstart",e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
lb.addEventListener("touchend",e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;
if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)korak(dx<0?1:-1)},{passive:true})}
function prikazi(i){tren=i;const r=G.radovi[G.red[i]];slike.innerHTML="";
r.slike.forEach(([src,w,h],n)=>{const im=new Image();im.src=src;im.width=w;im.height=h;im.decoding="async";
im.alt=r.alt+(r.slike.length>1?" ("+(n+1)+"/"+r.slike.length+")":"");slike.appendChild(im)});
slike.scrollTop=0;naslov.textContent=r.naslov;opis.textContent=r.opis;meta.textContent=r.tool+" · "+r.oznaka;
broj.textContent=(i+1)+" / "+G.red.length;const sled=G.radovi[G.red[(i+1)%G.red.length]];new Image().src=sled.slike[0][0]}
function otvori(slug,izvor){if(!lb)napravi();pre=izvor;prikazi(G.red.indexOf(slug));lb.hidden=false;lb.classList.add("otvoren");
document.body.classList.add("zakljucan");lb.querySelector(".lb-x").focus()}
function zatvori(){lb.hidden=true;lb.classList.remove("otvoren");document.body.classList.remove("zakljucan");slike.innerHTML="";
if(pre)pre.focus({preventScroll:true})}
function korak(d){prikazi((tren+d+G.red.length)%G.red.length)}
document.querySelectorAll(".folders [data-lb]").forEach(b=>b.addEventListener("click",()=>otvori(b.dataset.lb,b)));
document.addEventListener("keydown",e=>{if(!lb||lb.hidden)return;
if(e.key==="Escape")zatvori();else if(e.key==="ArrowRight")korak(1);else if(e.key==="ArrowLeft")korak(-1);
else if(e.key==="Tab"){const f=[...lb.querySelectorAll("button")],a=f.indexOf(document.activeElement);
if(e.shiftKey&&a<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&a===f.length-1){e.preventDefault();f[0].focus()}}})})();
