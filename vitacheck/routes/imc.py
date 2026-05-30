from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from decorators import login_required

imc_bp = Blueprint('imc', __name__)

def calcular_clasificacion(valor):
    if valor < 18.5:   return "Bajo peso"
    if valor < 25.0:   return "Normal"
    if valor < 30.0:   return "Sobrepeso"
    if valor < 35.0:   return "Obesidad I"
    if valor < 40.0:   return "Obesidad II"
    return "Obesidad III"

@imc_bp.route("/imc", methods=["GET", "POST"])
@login_required
def imc():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    resultado = None

    if request.method == "POST":
        paciente_id  = request.form.get("paciente_id")
        peso         = float(request.form.get("peso"))
        altura       = float(request.form.get("altura"))
        valor_imc    = round(peso / (altura ** 2), 2)
        clasificacion = calcular_clasificacion(valor_imc)

        cur.execute("SELECT recomendacion FROM categorias WHERE nombre=%s", (clasificacion,))
        cat = cur.fetchone()
        recomendacion = cat["recomendacion"] if cat else "Mantener control médico constante."

        try:
            cur.execute("""
                INSERT INTO imc_historial (paciente_id, peso, altura, imc, clasificacion)
                VALUES (%s,%s,%s,%s,%s)
            """, (paciente_id, peso, altura, valor_imc, clasificacion))
            conn.commit()
            resultado = dict(paciente_id=paciente_id, imc=valor_imc,
                             clasificacion=clasificacion, peso=peso,
                             altura=altura, recomendacion=recomendacion)
            flash("IMC guardado exitosamente.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    lista_pacientes = cur.fetchall()
    cur.close(); conn.close()
    return render_template("imc.html", pacientes=lista_pacientes, resultado=resultado)


@imc_bp.route("/paciente/<int:paciente_id>/imc/historial")
@login_required
def imc_historial_paciente(paciente_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, nombre FROM pacientes WHERE id=%s", (paciente_id,))
    paciente = cur.fetchone()

    if not paciente:
        flash("Paciente no encontrado.", "danger")
        cur.close(); conn.close()
        return redirect(url_for("imc.imc"))

    cur.execute("""
        SELECT id, peso, altura, imc, clasificacion, fecha
        FROM imc_historial WHERE paciente_id=%s ORDER BY fecha ASC
    """, (paciente_id,))
    historial_asc = cur.fetchall()
    cur.close(); conn.close()

    labels      = [r["fecha"].strftime("%d/%m/%Y") if hasattr(r["fecha"], "strftime") else str(r["fecha"]) for r in historial_asc]
    imc_values  = [float(r["imc"])  for r in historial_asc]
    peso_values = [float(r["peso"]) for r in historial_asc]

    return render_template("imc_historial.html", paciente=paciente,
                           historial=list(reversed(historial_asc)),
                           labels=labels, imc_values=imc_values, peso_values=peso_values)


@imc_bp.route("/actividad", methods=["GET", "POST"])
@login_required
def actividad():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    paciente_seleccionado = None
    ultimo_imc = None

    paciente_id = request.args.get("paciente_id") or request.form.get("paciente_id")
    if paciente_id:
        cur.execute("SELECT id, nombre FROM pacientes WHERE id=%s", (paciente_id,))
        paciente_seleccionado = cur.fetchone()
        if paciente_seleccionado:
            cur.execute("""
                SELECT imc, clasificacion FROM imc_historial
                WHERE paciente_id=%s ORDER BY fecha DESC LIMIT 1
            """, (paciente_id,))
            ultimo_imc = cur.fetchone()

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    lista_pacientes = cur.fetchall()
    cur.close(); conn.close()
    return render_template("actividad.html", pacientes=lista_pacientes,
                           paciente_seleccionado=paciente_seleccionado, ultimo_imc=ultimo_imc)
