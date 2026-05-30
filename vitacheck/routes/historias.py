from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_connection
from decorators import login_required

historias_bp = Blueprint('historias', __name__)

@historias_bp.route("/paciente/<int:patient_id>/historias")
@login_required
def historias(patient_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, nombre FROM pacientes WHERE id=%s", (patient_id,))
    paciente = cur.fetchone()
    cur.execute("""
        SELECT h.*, u.nombre_completo AS medico_nombre
        FROM historias_clinicas h
        LEFT JOIN usuarios u ON h.medico_id = u.id
        WHERE h.paciente_id=%s ORDER BY h.fecha DESC
    """, (patient_id,))
    lista = cur.fetchall()
    cur.close(); conn.close()
    return render_template("historias.html", paciente=paciente, historias=lista)


@historias_bp.route("/paciente/<int:patient_id>/historia/nueva", methods=["GET", "POST"])
@login_required
def historia_nueva(patient_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)

    if request.method == "POST":
        cur.execute("""
            INSERT INTO historias_clinicas (paciente_id, medico_id, tipo, nota)
            VALUES (%s,%s,%s,%s)
        """, (patient_id, session["user"]["id"], request.form.get("tipo"), request.form.get("nota")))
        conn.commit()
        flash("Historia clínica registrada.", "success")
        cur.close(); conn.close()
        return redirect(url_for("historias.historias", patient_id=patient_id))

    cur.close(); conn.close()
    return render_template("historia_form.html", paciente_id=patient_id)
