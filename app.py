from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

SHEETS_API_URL = "https://script.google.com/macros/s/AKfycbzWBl4YmveBKCHRLXWh9RAbmedCRd7f5z8pPncMjCQz4ictUpukyc1ZiQzbm4IDHU8MGw/exec"

@app.route("/borrar/<int:id>", methods=["POST"])
def borrar(id):
    pin = request.form.get("pin")

    params = {
        "id": id,
        "pin": pin
    }

    requests.delete(SHEETS_API_URL, params=params)
    return redirect("/")

def index():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        monto = float(request.form["monto"])

        if not nombre or monto <= 0:
            return redirect("/")

        data = {
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "nombre": nombre,
            "monto": monto
        }

        requests.post(SHEETS_API_URL, json=data)
        return redirect("/")

    response = requests.get(SHEETS_API_URL)
    ahorros = response.json()
    for i, a in enumerate(ahorros, start=1):
        a["id"]=i

    total = sum(a["monto"] for a in ahorros)

    por_persona = {}
    for a in ahorros:
        por_persona[a["nombre"]] = por_persona.get(a["nombre"], 0) + a["monto"]

    return render_template(
        "index.html",
        ahorros=ahorros,
        total=total,
        por_persona=por_persona
    )

if __name__ == "__main__":
    app.run()

