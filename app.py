from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- BASE DE DATOS ----------
def get_db_connection():
    conn = sqlite3.connect("ahorros.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ahorros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()
# ----------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        monto = float(request.form["monto"])

        if not nombre or monto <= 0:
            conn.close()
            return redirect("/")

        fecha = datetime.now().strftime("%d/%m/%Y")

        conn.execute(
            "INSERT INTO ahorros (nombre, monto, fecha) VALUES (?, ?, ?)",
            (nombre, monto, fecha)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    ahorros = conn.execute("SELECT * FROM ahorros").fetchall()

    # Total general
    total = sum(a["monto"] for a in ahorros)

    # Total por persona
    por_persona = {}
    for a in ahorros:
        nombre = a["nombre"]
        por_persona[nombre] = por_persona.get(nombre, 0) + a["monto"]

    conn.close()

    return render_template(
        "index.html",
        ahorros=ahorros,
        total=total,
        por_persona=por_persona
    )


if __name__ == "__main__":
    app.run()
