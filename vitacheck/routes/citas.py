from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from decorators import login_required

citas_bp = Blueprint('citas', __name__)

@citas_bp.route("/citas")
@login_required
def citas():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.*, p.nombre AS paciente_nombre, m.nombre AS medico_nombre
        FROM citas c
        JOIN pacientes p ON c.paciente_id = p.id
        JOIN medicos   m ON c.medico_id   = m.id
        ORDER BY c.fecha DESC, c.hora DESC
    """)
    lista = cur.fetchall()
    cur.close(); conn.close()
    return render_template("citas.html", citas=lista)


@citas_bp.route("/citas/nueva", methods=["GET", "POST"])
@login_required
def cita_nueva():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            cur.execute("""
                INSERT INTO citas (paciente_id, medico_id, fecha, hora, motivo)
                VALUES (%s,%s,%s,%s,%s)
            """, (request.form.get("paciente_id"), request.form.get("medico_id"),
                  request.form.get("fecha"), request.form.get("hora"), request.form.get("motivo")))
            conn.commit()
            flash("Cita agendada correctamente.", "success")
            return redirect(url_for("citas.citas"))
        except Exception:
            conn.rollback()
            flash("Error al agendar la cita.", "danger")
        finally:
            cur.close(); conn.close()

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    pacientes = cur.fetchall()
    cur.execute("SELECT id, nombre FROM medicos ORDER BY nombre ASC")
    medicos = cur.fetchall()
    cur.close(); conn.close()
    return render_template("cita_form.html", cita=None, pacientes=pacientes, medicos=medicos)


@citas_bp.route("/citas/borrar/<int:id>", methods=["POST"])
@login_required
def cita_borrar(id):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM citas WHERE id=%s", (id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Cita cancelada.", "warning")
    return redirect(url_for("citas.citas"))


@citas_bp.route("/citas/cambiar_estado/<int:id>", methods=["POST"])
@login_required
def cita_cambiar_estado(id):
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("UPDATE citas SET estado=%s WHERE id=%s", (request.form.get("estado"), id))
        conn.commit()
        flash("Estado actualizado.", "success")
    except Exception:
        conn.rollback()
        flash("Error al cambiar el estado.", "danger")
    finally:
        cur.close(); conn.close()
    return redirect(url_for("citas.citas"))
