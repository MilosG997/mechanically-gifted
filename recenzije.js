// "Šta kažu klijenti": recenzije sa Google-a preko /.netlify/functions/reviews (učitava se tek kad se priđe sekciji).
// Dok nema recenzija (ili API ne odgovori) ostaje mala traka "Ostavite recenziju"; čim ih ima, crta se cela sekcija.
(()=>{const sec=document.getElementById("recenzije");if(!sec)return;
const L=JSON.parse(sec.dataset.tekst);let uradjeno=false;
function el(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
function zvezde(n){const s=el("div","rev-stars");s.setAttribute("aria-label",L.ocena.replace("{n}",n));
for(let i=1;i<=5;i++){const z=el("span",i<=Math.round(n)?"":"rev-off","★");z.setAttribute("aria-hidden","true");s.appendChild(z)}return s}
function gLogo(w){const s=document.createElementNS("http://www.w3.org/2000/svg","svg");s.setAttribute("width",w);s.setAttribute("height",w);
s.setAttribute("aria-hidden","true");const u=document.createElementNS("http://www.w3.org/2000/svg","use");u.setAttribute("href","#revG");s.appendChild(u);return s}
function inicijali(ime){return ime.split(/\s+/).filter(Boolean).slice(0,2).map(p=>p[0]).join("").toUpperCase()||"?"}
function broj(n){return L.lang==="sr"?(n%10>=1&&n%10<=4&&!(n%100>=11&&n%100<=14)?L.cnt1:L.cnt5):(n===1?L.cnt1:L.cnt5)}
function kartica(r){const a=el("article","rev-card");const q=el("div","rev-q","“");q.setAttribute("aria-hidden","true");a.appendChild(q);
const top=el("div","rev-top");let av;
if(r.photo){av=el("img","rev-av");av.src=r.photo;av.alt="";av.width=42;av.height=42;av.referrerPolicy="no-referrer";
av.onerror=()=>{const z=el("div","rev-av",inicijali(r.author));av.replaceWith(z)}}else av=el("div","rev-av",inicijali(r.author));
const who=el("div","rev-who");who.appendChild(el("b",null,r.author));who.appendChild(el("span",null,r.time));
const gm=gLogo(22);gm.setAttribute("class","rev-gm");top.append(av,who,gm);a.append(top,zvezde(r.rating));
const t=el("p","rev-txt",r.text);if(r.lang)t.lang=r.lang;a.appendChild(t);
const vise=el("button","rev-vise",L.vise);vise.type="button";vise.hidden=true;
vise.onclick=()=>{const otv=t.classList.toggle("open");vise.textContent=otv?L.manje:L.vise};a.appendChild(vise);
if(r.link){const l=el("a","rev-more",L.link);l.href=r.link;l.target="_blank";l.rel="noopener";a.appendChild(l)}
requestAnimationFrame(()=>{vise.hidden=t.scrollHeight<=t.clientHeight+2});return a}
function nacrtaj(d){const w=el("div","w");
const eye=el("div","eye",L.eye),h=el("h2",null,L.naslov);
const sum=el("div","rev-sum"),score=el("div","rev-score"),g=el("div","rev-g");g.appendChild(gLogo(24));
const info=el("div");info.append(zvezde(d.rating||0),el("div","rev-cnt",broj(d.userRatingCount).replace("{n}",d.userRatingCount)));
score.append(g,el("div","rev-big",(d.rating||0).toFixed(1).replace(".",L.lang==="sr"?",":".")),info);
const acts=sec.querySelector(".rev-acts").cloneNode(true);acts.querySelector(".rev-svi").hidden=false;sum.append(score,acts);
const wrap=el("div","rev-wrap"),track=el("div","rev-track"),nav=el("div","rev-nav"),dots=el("div","rev-dots"),arr=el("div","rev-arrows");
track.tabIndex=0;track.setAttribute("aria-label",L.naslov);d.reviews.forEach(r=>{track.appendChild(kartica(r));dots.appendChild(el("i"))});
const pre=el("button",null,"‹"),sled=el("button",null,"›");pre.type=sled.type="button";pre.setAttribute("aria-label",L.pre);sled.setAttribute("aria-label",L.sled);
arr.append(pre,sled);nav.append(dots,arr);wrap.append(track,nav);
const src=el("div","rev-src");src.append(gLogo(16),document.createTextNode(L.izvor));
w.append(eye,h,sum,wrap,src);sec.classList.remove("rev-mala");sec.replaceChildren(w);
const kar=[...track.children],tacke=[...dots.children],korak=()=>kar[0].offsetWidth+16;
function upd(){const i=Math.round(track.scrollLeft/korak());tacke.forEach((t,k)=>t.classList.toggle("on",k===Math.min(i,tacke.length-1)));
const ima=track.scrollWidth>track.clientWidth+2;nav.hidden=!ima}
track.addEventListener("scroll",upd,{passive:true});addEventListener("resize",upd);upd();
sled.onclick=()=>track.scrollBy({left:korak()});pre.onclick=()=>track.scrollBy({left:-korak()})}
function ucitaj(){if(uradjeno)return;uradjeno=true;
const rucno=sec.dataset.rucno?JSON.parse(sec.dataset.rucno):null,ima=d=>d&&d.reviews&&d.reviews.length;
// API (kad je ključ podešen) ima prednost; inače recenzije prepisane u napravi-sajt.py
fetch("/.netlify/functions/reviews?lang="+L.lang).then(r=>r.ok?r.json():null).catch(()=>null).then(d=>{if(ima(d))nacrtaj(d);else if(ima(rucno))nacrtaj(rucno)})}
if("IntersectionObserver"in window){const io=new IntersectionObserver(e=>{if(e.some(x=>x.isIntersecting)){io.disconnect();ucitaj()}},{rootMargin:"800px"});io.observe(sec)}
else addEventListener("load",ucitaj)})();
