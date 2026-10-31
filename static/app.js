const formulaire = document.getElementById("formulaire");
const champ = document.getElementById("sms");
const bouton = document.getElementById("bouton");
const zone = document.getElementById("resultat");

document.querySelectorAll(".exemple").forEach((b) => {
  b.addEventListener("click", () => {
    champ.value = b.dataset.sms;
    champ.focus();
  });
});

function el(tag, classe, texte) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (texte !== undefined && texte !== null) e.textContent = texte;
  return e;
}

function classeVerdict(v) {
  if (v === "RISQUE ÉLEVÉ") return "eleve";
  if (v === "RISQUE À VÉRIFIER") return "verifier";
  return "neutre";
}

function afficher(r) {
  zone.replaceChildren();
  zone.hidden = false;

  if (!r.ok) {
    zone.appendChild(el("p", "erreur", r.erreur || "Une erreur est survenue."));
    return;
  }

  zone.appendChild(el("h2", "verdict " + classeVerdict(r.verdict), r.verdict));
  zone.appendChild(el("p", "", r.resume));

  const infos = el("ul", "infos");
  [
    ["Montant annoncé", r.montant],
    ["Expéditeur déclaré", r.expediteur],
    ["Type de transaction", r.type_transaction],
  ].forEach(([nom, val]) => {
    infos.appendChild(el("li", "", nom + " : " + (val || "non précisé")));
  });
  zone.appendChild(infos);

  if (r.indices.length) {
    zone.appendChild(el("h3", "", "Indices détectés"));
    const liste = el("ul");
    r.indices.forEach((i) => {
      const li = el("li");
      if (typeof i === "string") {
        li.textContent = i;
      } else {
        li.appendChild(el("strong", "", String(i.indice || "")));
        li.appendChild(el("span", "", " — " + String(i.explication || "")));
      }
      liste.appendChild(li);
    });
    zone.appendChild(liste);
  }

  if (r.conseils.length) {
    zone.appendChild(el("h3", "", "Que faire ?"));
    const liste = el("ul");
    r.conseils.forEach((c) => liste.appendChild(el("li", "", String(c))));
    zone.appendChild(liste);
  }

  zone.appendChild(el("p", "avertissement", r.avertissement));
}

formulaire.addEventListener("submit", async (e) => {
  e.preventDefault();
  bouton.disabled = true;
  bouton.textContent = "Analyse en cours...";
  try {
    const rep = await fetch("/analyser", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sms: champ.value }),
    });
    afficher(await rep.json());
  } catch (err) {
    afficher({ ok: false, erreur: "Impossible de contacter le serveur." });
  } finally {
    bouton.disabled = false;
    bouton.textContent = "Analyser";
  }
});