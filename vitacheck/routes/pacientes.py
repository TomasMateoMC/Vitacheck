from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from decorators import login_required

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route("/dashboard")
@login_required
def dashboard():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM pacientes ORDER BY nombre ASC")
    lista = cur.fetchall()
    cur.close(); conn.close()
    return render_template("pacientes.html", pacientes=lista)


@pacientes_bp.route("/pacientes/nuevo", methods=["GET", "POST"])
@pacientes_bp.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def guardar_paciente(id=None):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    paciente = None

    if id:
        cur.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
        paciente = cur.fetchone()

    if request.method == "POST":
        nombre          = request.form.get("nombre", "").strip()
        documento       = request.form.get("documento", "").strip()
        fecha_nacimiento= request.form.get("fecha_nacimiento")
        genero          = request.form.get("genero")
        grupo_sanguineo = request.form.get("grupo_sanguineo")
        telefono        = request.form.get("telefono", "").strip()
        email           = request.form.get("email", "").strip()
        direccion       = request.form.get("direccion", "").strip()
        alergias        = request.form.get("alergias", "").strip()

        if not documento:
            flash("El documento no puede estar vacío.", "danger")
            cur.close(); conn.close()
            return render_template("paciente_form.html", paciente=paciente)

        try:
            if id:
                cur.execute("SELECT id FROM pacientes WHERE documento=%s AND id!=%s", (documento, id))
            else:
                cur.execute("SELECT id FROM pacientes WHERE documento=%s", (documento,))

            if cur.fetchone():
                flash("El documento ya existe.", "danger")
                cur.close(); conn.close()
                return render_template("paciente_form.html", paciente=paciente)

            if id:
                cur.execute("""
                    UPDATE pacientes SET nombre=%s, documento=%s, fecha_nacimiento=%s,
                    telefono=%s, email=%s, direccion=%s, genero=%s, grupo_sanguineo=%s, alergias=%s
                    WHERE id=%s
                """, (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias, id))
                flash("Paciente actualizado.", "success")
            else:
                cur.execute("""
                    INSERT INTO pacientes (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias))
                flash("Paciente registrado.", "success")

            conn.commit()
            cur.close(); conn.close()
            return redirect(url_for("pacientes.pacientes"))

        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
            cur.close(); conn.close()
            return render_template("paciente_form.html", paciente=paciente)

    cur.close(); conn.close()
    return render_template("paciente_form.html", paciente=paciente)


@pacientes_bp.route("/pacientes/borrar/<int:id>", methods=["POST"])
@login_required
def paciente_borrar(id):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM pacientes WHERE id=%s", (id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Paciente eliminado.", "warning")
    return redirect(url_for("pacientes.pacientes"))
