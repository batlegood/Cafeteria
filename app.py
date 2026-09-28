from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "clave_secreta"

# 🔑 Conexión a SQL Server (asegúrate de tener instalado ODBC Driver 17)
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=localhost\\SQLEXPRESS01;Database=CafeteriaPOS;Trusted_Connection=yes;"

# Ruta raíz: redirige al formulario
@app.route("/")
def home():
    return redirect(url_for("registrar_cliente"))

# Ruta para registrar clientes
@app.route("/registrar_cliente", methods=["GET", "POST"])
def registrar_cliente():
    if request.method == "POST":
        cedula = request.form["cedula"]
        nombre = request.form["nombre"]
        correo = request.form["correo"]

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Clientes (Cedula, Nombre, Correo)
                VALUES (?, ?, ?)
            """, (cedula, nombre, correo))
            conn.commit()
            conn.close()
            flash("Cliente registrado exitosamente ✅", "success")
            return redirect(url_for("registrar_cliente"))
        except Exception as e:
            flash(f"Error al registrar cliente: {e}", "danger")

    return render_template("registrar_cliente.html")

# Bloque de arranque
if __name__ == "__main__":
    app.run(debug=True)
