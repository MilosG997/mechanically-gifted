// Portfolio: filteri bez učitavanja stranice + lightbox galerija (strelice, Esc, klik van slike, swipe).
(()=>{const podaci=document.getElementById("galerija");if(!podaci)return;
const G=JSON.parse(podaci.textContent),kartice=[...document.querySelectorAll(".work .case")],R=matchMedia("(prefers-reduced-motion: reduce)").matches;
let filter="sve";
// Filteri
document.querySelectorAll(".filteri [data-filter]").forEach(b=>b.addEventListener("click",()=>{
filter=b.dataset.filter;document.querySelectorAll(".filteri [data-filter]").forEach(x=>x.setAttribute("aria-pressed",x===b));
const vidi=k=>filter==="sve"||k.dataset.kat===filter;
kartice.forEach(k=>{if(!vidi(k)&&!k.hidden)k.classList.add("skriva")});
setTimeout(()=>kartice.forEach(k=>{const v=vidi(k);k.classList.remove("skriva","ulazi");if(v&&k.hidden){k.hidden=false;void k.offsetWidth;k.classList.add("ulazi")}k.hidden=!v}),R?0:200)}));
// Lightbox
const lb=document.getElementById("lb"),slike=document.getElementById("lbSlike"),naslov=document.getElementById("lbNaslov"),
opis=document.getElementById("lbOpis"),alat=document.getElementById("lbAlat"),broj=document.getElementById("lbBroj");
let tren=0,pre=null;
const vidljivi=()=>kartice.map((k,i)=>k.hidden?-1:i).filter(i=>i>=0);
function prikazi(i){tren=i;const r=G[i],v=vidljivi(),poz=v.indexOf(i)+1;
slike.innerHTML="";r.slike.forEach(([src,w,h],n)=>{const im=new Image();im.src=src;im.width=w;im.height=h;im.decoding="async";
im.alt=r.alt+(r.slike.length>1?" ("+(n+1)+"/"+r.slike.length+")":"");slike.appendChild(im)});
slike.scrollTop=0;naslov.textContent=r.naslov;opis.textContent=r.opis;alat.textContent=r.alat;broj.textContent=poz+" / "+v.length;
const sled=G[v[(v.indexOf(i)+1)%v.length]];if(sled){const p=new Image();p.src=sled.slike[0][0]}}
function otvori(i,izvor){pre=izvor||document.activeElement;prikazi(i);lb.hidden=false;lb.classList.add("otvoren");document.body.classList.add("zakljucan");
lb.querySelector(".lb-x").focus();window.mgEvent&&mgEvent("portfolio_open",{project:G[i].naslov})}
function zatvori(){lb.hidden=true;lb.classList.remove("otvoren");document.body.classList.remove("zakljucan");slike.innerHTML="";if(pre&&pre.focus)pre.focus({preventScroll:true})}
function korak(d){const v=vidljivi(),p=v.indexOf(tren);prikazi(v[(p+d+v.length)%v.length])}
document.querySelectorAll(".work [data-lb]").forEach(b=>b.addEventListener("click",()=>otvori(+b.dataset.lb,b)));
lb.querySelector(".lb-x").addEventListener("click",zatvori);
lb.querySelector(".lb-pre").addEventListener("click",()=>korak(-1));
lb.querySelector(".lb-sled").addEventListener("click",()=>korak(1));
lb.addEventListener("click",e=>{if(e.target===lb)zatvori()});
document.addEventListener("keydown",e=>{if(lb.hidden)return;
if(e.key==="Escape")zatvori();else if(e.key==="ArrowRight")korak(1);else if(e.key==="ArrowLeft")korak(-1);
else if(e.key==="Tab"){const f=[...lb.querySelectorAll("button")],a=f.indexOf(document.activeElement);
if(e.shiftKey&&a<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&a===f.length-1){e.preventDefault();f[0].focus()}}});
// swipe levo/desno na telefonu (vertikalno pomeranje ostaje za dugačke stranice)
let x0=null,y0=0;lb.addEventListener("touchstart",e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
lb.addEventListener("touchend",e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;
if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)korak(dx<0?1:-1)},{passive:true})})();
