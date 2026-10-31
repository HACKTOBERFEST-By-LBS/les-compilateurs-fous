from flask import Flask, jsonify, render_template, request

from analyseur import analyser_sms

app = Flask(__name__)


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/analyser", methods=["POST"])
def analyser():
    donnees = request.get_json(silent=True) or {}
    sms = donnees.get("sms")
    if not isinstance(sms, str):
        sms = ""
    resultat = analyser_sms(sms)
    return jsonify(resultat), (200 if resultat.get("ok") else 400)


if __name__ == "__main__":
    app.run(debug=True)