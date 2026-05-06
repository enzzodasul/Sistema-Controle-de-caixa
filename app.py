from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

ARQUIVO = "dados.json"


def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {}
    with open(ARQUIVO, "r") as f:
        return json.load(f)


def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


def gerar_mes(ano, mes):
    dias = []
    data = datetime(ano, mes, 1)

    while data.month == mes:
        dias.append({
            "dia": data.day,
            "data": data.strftime("%d/%m/%Y"),
            "semana": data.strftime("%A")
        })
        data += timedelta(days=1)

    return dias


@app.route("/")
def index():
    ano = 2024
    mes = 4

    dias = gerar_mes(ano, mes)
    dados = carregar_dados()

    for d in dias:
        chave = f"{ano}-{mes}-{d['dia']}"
        if chave in dados:
            d.update(dados[chave])
        else:
            d.update({
                "dinheiro": "",
                "pix": "",
                "credito": "",
                "debito": "",
                "sangria": "",
                "total": ""
            })

    return render_template("index.html", dias=dias)


@app.route("/salvar", methods=["POST"])
def salvar():
    dados = carregar_dados()

    for i in range(1, 32):
        dinheiro = request.form.get(f"dinheiro{i}") or "0"
        pix = request.form.get(f"pix{i}") or "0"
        credito = request.form.get(f"credito{i}") or "0"
        debito = request.form.get(f"debito{i}") or "0"
        sangria = request.form.get(f"sangria{i}") or "0"

        total = float(dinheiro) + float(pix) + float(credito) + float(debito) - float(sangria)

        chave = f"2024-4-{i}"

        dados[chave] = {
            "dinheiro": dinheiro,
            "pix": pix,
            "credito": credito,
            "debito": debito,
            "sangria": sangria,
            "total": round(total, 2)
        }

    salvar_dados(dados)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)