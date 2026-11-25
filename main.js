// One Logo In: small progressive enhancements. The page works without this file.
document.documentElement.classList.remove("no-js");

/* ---------- Headline A/B preview (?h=a | ?h=b) ---------- */
const title = document.getElementById("hero-title");
const variantCards = document.querySelectorAll(".variant");

function setHeadline(v, { animate = true } = {}) {
  if (!["a", "b"].includes(v)) v = "a";
  title.dataset.variant = v;
  title.querySelectorAll("[data-h]").forEach((s) => (s.hidden = s.dataset.h !== v));
  variantCards.forEach((c) => c.classList.toggle("is-on", c.dataset.set === v));
  if (animate) {
    title.classList.remove("swap");
    void title.offsetWidth; // restart animation
    title.classList.add("swap");
  }
  const url = new URL(location.href);
  v === "a" ? url.searchParams.delete("h") : url.searchParams.set("h", v);
  history.replaceState(null, "", url);
}

setHeadline(new URLSearchParams(location.search).get("h") || "a", { animate: false });

variantCards.forEach((card) =>
  card.addEventListener("click", () => {
    setHeadline(card.dataset.set);
    title.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
  })
);

/* ---------- Prompt anatomy: focus one part ---------- */
const anatomy = document.getElementById("anatomy");
if (anatomy) {
  const keys = anatomy.querySelectorAll(".anatomy__legend button");
  const segs = anatomy.querySelectorAll(".seg");
  let active = null;
  const focus = (k) => {
    active = k;
    anatomy.classList.toggle("is-focus", !!k);
    keys.forEach((b) => b.classList.toggle("is-on", b.dataset.k === k));
    segs.forEach((s) => s.classList.toggle("is-on", s.dataset.k === k));
  };
  keys.forEach((b) => {
    b.addEventListener("mouseenter", () => focus(b.dataset.k));
    b.addEventListener("focus", () => focus(b.dataset.k));
    b.addEventListener("click", () => focus(active === b.dataset.k ? null : b.dataset.k));
  });
  anatomy.querySelector(".anatomy__legend").addEventListener("mouseleave", () => focus(null));
}

/* ---------- Proof sheet reveal ---------- */
const sheet = document.getElementById("sheet");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && (sheet.classList.add("in"), io.disconnect())),
    { threshold: 0.12 }
  );
  io.observe(sheet);
  sheet.querySelectorAll(".tile").forEach((t, i) => (t.style.transitionDelay = `${i * 60}ms`));
} else {
  sheet.classList.add("in");
}

/* ---------- Proof viewer ---------- */
const viewer = document.getElementById("viewer");
let assets = null;

async function loadAssets() {
  if (assets) return assets;
  const res = await fetch("data/assets.json");
  assets = Object.fromEntries((await res.json()).map((a) => [a.id, a]));
  return assets;
}

async function openViewer(id) {
  const data = await loadAssets().catch(() => null);
  const a = data && data[id];
  if (!a) return;
  const img = document.getElementById("viewer-img");
  img.src = `assets/img/${a.slug}.jpg`;
  img.alt = sheet.querySelector(`[data-id="${id}"] img`)?.alt || a.channel;
  document.getElementById("viewer-meta").textContent =
    `${a.ratio} · ${a.model} · ${a.rendering} · seed ${a.seed}`;
  document.getElementById("viewer-title").textContent = `${a.channel}: ${a.purpose}`;
  document.getElementById("viewer-prompt").textContent = a.prompt;
  const kept = document.getElementById("viewer-kept");
  kept.replaceChildren(...a.keptTheSame.map((t) => Object.assign(document.createElement("li"), { textContent: t })));
  viewer.showModal();
}

sheet.addEventListener("click", (e) => {
  const tile = e.target.closest(".tile");
  if (tile) openViewer(tile.dataset.id);
});
viewer.addEventListener("click", (e) => {
  if (e.target === viewer) viewer.close(); // click on backdrop
});
