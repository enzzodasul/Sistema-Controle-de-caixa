@app.route("/salvar", methods=["POST"])
def salvar():
    dados = []

    for i in range(1, 31):
        dinheiro = float(request.form.get(f"dinheiro{i}") or 0)
        pix = float(request.form.get(f"pix{i}") or 0)
        credito = float(request.form.get(f"credito{i}") or 0)
        debito = float(request.form.get(f"debito{i}") or 0)
        sangria = float(request.form.get(f"sangria{i}") or 0)

        total = dinheiro + pix + credito + debito - sangria

        dados.append({
            "dia": i,
            "dinheiro": dinheiro,
            "pix": pix,
            "credito": credito,
            "debito": debito,
            "sangria": sangria,
            "total": total
        })

    salvar_dados(dados)

    return redirect("/")