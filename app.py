from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Conexión a SQL Server
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=localhost\\SQLEXPRESS01;Database=CafeteriaPOS;Trusted_Connection=yes;"

# Validación de cédula colombiana
def validar_cedula(cedula: str) -> bool:
    # Debe ser numérica
    if not cedula.isdigit():
        return False

    # Solo se permiten longitudes de 6, 8 o 10
    if len(cedula) in [6, 8]:
        return True
    elif len(cedula) == 10:
        # Si es de 10 dígitos, debe comenzar con '1'
        return cedula.startswith("1")
    else:
        # Cualquier otra longitud (menor de 6, 7, 9 o mayor de 10) no es válida
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

        # Validación de cédula
        if not validar_cedula(cedula):
            flash("Cédula inválida. Solo se permiten 6, 8 o 10 dígitos. Si es de 10, debe comenzar con 1.", "danger")
            return render_template("registrar_cliente.html")

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
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

# Bloque de arranque
if __name__ == "__main__":
    app.run(debug=True)


