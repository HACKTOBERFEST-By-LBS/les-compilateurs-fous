import json

from analyseur import analyser_sms

EXEMPLES = {
    "Faux dépôt par erreur": "Vous avez recu 25000 FCFA par erreur. Renvoyez-moi vite cet argent au 90 00 00 00 svp, c'est urgent, je suis dans l'embarras.",
    "Faux gain": "FELICITATIONS ! Vous avez gagné 500000 FCFA au grand concours. Envoyez votre code secret et 5000 FCFA de frais pour recevoir votre gain: http://gain-moov.example",
    "Message banal": "Salut, on se voit demain à 18h au marché ? Apporte la liste.",
}

for titre, sms in EXEMPLES.items():
    print("=" * 60)
    print(titre)
    print(json.dumps(analyser_sms(sms), ensure_ascii=False, indent=2))