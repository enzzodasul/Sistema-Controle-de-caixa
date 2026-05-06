from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ARQUIVO = "dados.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

@app.route("/")
def index():
    dados = carregar_dados()
    total = sum(item["total"] for item in dados)
    return render_template("index.html", dados=dados, total=total)

@app.route("/salvar", methods=["POST"])
def salvar():
    dinheiro = float(request.form["dinheiro"])
    credito = float(request.form["credito"])
    debito = float(request.form["debito"])
    pix = float(request.form["pix"])
    sangria = float(request.form["sangria"])

    total = dinheiro + credito + debito + pix - sangria

    dados = carregar_dados()

    dados.append({
        "dinheiro": dinheiro,
        "credito": credito,
        "debito": debito,
        "pix": pix,
        "sangria": sangria,
        "total": total
    })

    salvar_dados(dados)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)