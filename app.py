from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta"

def get_connection():
    return sqlite3.connect("cafeteria.db")

def validar_cedula(cedula: str) -> bool:
    if not cedula.isdigit():
        return False
    if len(cedula) in [6, 8]:
        return True
    elif len(cedula) == 10:
        return cedula.startswith("1")
    else:
        return False

@app.route("/")
def home():
    return redirect(url_for("registrar_cliente"))

@app.route("/registrar_cliente", methods=["GET", "POST"])
def registrar_cliente():
    if request.method == "POST":
        cedula = request.form["cedula"]
        nombre = request.form["nombre"]
        correo = request.form["correo"]

        if not validar_cedula(cedula):
            flash("Cédula inválida. Solo se permiten 6, 8 o 10 dígitos. Si es de 10, debe comenzar con 1.", "danger")
            return render_template("registrar_cliente.html")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Clientes (
                    Cedula TEXT PRIMARY KEY,
                    Nombre TEXT,
                    Correo TEXT
                )
            """)
            cursor.execute("""
                INSERT INTO Clientes (Cedula, Nombre, Correo)
                VALUES (?, ?, ?)
            """, (cedula, nombre, correo))
            conn.commit()
            flash("Cliente registrado exitosamente", "success")
        except Exception as e:
            flash(f"Error al registrar cliente: {e}", "danger")
        finally:
            conn.close()

    return render_template("registrar_cliente.html")

if __name__ == "__main__":
    app.run(debug=True)
