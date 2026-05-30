from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from decorators import login_required

medicos_bp = Blueprint('medicos', __name__)

@medicos_bp.route("/medicos")
@login_required
def medicos():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.*, e.nombre AS especialidad_nombre
        FROM medicos m LEFT JOIN especialidades e ON m.specialty_id = e.id
        ORDER BY m.nombre ASC
    """)
    lista = cur.fetchall()
    cur.close(); conn.close()
    return render_template("medicos.html", medicos=lista)


@medicos_bp.route("/medico/nuevo", methods=["GET", "POST"])
@login_required
def medico_nuevo():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM especialidades ORDER BY nombre ASC")
    especialidades = cur.fetchall()

    if request.method == "POST":
        try:
            cur.execute("""
                INSERT INTO medicos (nombre, numero_licencia, telefono, email, specialty_id)
                VALUES (%s,%s,%s,%s,%s)
            """, (request.form.get("nombre"), request.form.get("numero_licencia"),
                  request.form.get("telefono"), request.form.get("email"), request.form.get("specialty_id")))
            conn.commit()
            flash("Médico registrado exitosamente.", "success")
            cur.close(); conn.close()
            return redirect(url_for("medicos.medicos"))
        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")

    cur.close(); conn.close()
    return render_template("medico_form.html", medico=None, especialidades=especialidades)


@medicos_bp.route("/medicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def medico_editar(id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            cur.execute("""
                UPDATE medicos SET nombre=%s, numero_licencia=%s, telefono=%s, email=%s, specialty_id=%s
                WHERE id=%s
            """, (request.form.get("nombre"), request.form.get("numero_licencia"),
                  request.form.get("telefono"), request.form.get("email"),
                  request.form.get("specialty_id"), id))
            conn.commit()
            flash("Médico actualizado.", "success")
            return redirect(url_for("medicos.medicos"))
        except Exception:
            conn.rollback()
            flash("Error: la licencia ya pertenece a otro médico.", "danger")
        finally:
            cur.close(); conn.close()

    cur.execute("SELECT * FROM medicos WHERE id=%s", (id,))
    medico_actual = cur.fetchone()
    cur.execute("SELECT * FROM especialidades ORDER BY nombre ASC")
    especialidades = cur.fetchall()
    cur.close(); conn.close()
    return render_template("medico_form.html", medico=medico_actual, especialidades=especialidades)


@medicos_bp.route("/medicos/borrar/<int:id>", methods=["POST"])
@login_required
def medico_borrar(id):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM medicos WHERE id=%s", (id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Médico eliminado.", "warning")
    return redirect(url_for("medicos.medicos"))
