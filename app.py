from flask import Flask, jsonify, render_template, request

from analyseur import analyser_image, analyser_sms
from apprentissage import traiter_commande

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 Mo maximum

TYPES_IMAGE = {"image/png", "image/jpeg", "image/webp"}


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/analyser", methods=["POST"])
def analyser():
    texte = request.form.get("sms", "").strip()
    fichier = request.files.get("image")

    # Le mode apprentissage ne s'active QUE sur une commande qui commence par /
    if texte.startswith("/"):
        return jsonify(traiter_commande(texte, fichier))

    if fichier and fichier.filename:
        if fichier.mimetype not in TYPES_IMAGE:
            return jsonify({"ok": False, "erreur": "Format non accepté. Utilisez une image PNG, JPG ou WEBP."}), 400
        resultat = analyser_image(fichier.read(), fichier.mimetype)
    else:
        resultat = analyser_sms(texte)
    return jsonify(resultat), (200 if resultat.get("ok") else 400)


if __name__ == "__main__":
    app.run(debug=True)