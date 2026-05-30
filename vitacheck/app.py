# ------------------------------------------------------------
# IMPORTS & CONFIGURACIÓN
# ------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection
import functools
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "mi_clave_secreta_123")

# ------------------------------------------------------------
# DECORADOR DE PROTECCIÓN DE RUTAS
# ------------------------------------------------------------
def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            flash("Por favor, inicia sesión para acceder.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

# ------------------------------------------------------------
# 1. MÓDULO DE AUTENTICACIÓN (LOGIN / LOGOUT)
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user"] = user
            flash(f"¡Bienvenido, {user['nombre_completo']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ------------------------------------------------------------
# 2. MÓDULO DE PACIENTES
# ------------------------------------------------------------
@app.route("/pacientes")
@login_required
def pacientes():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM pacientes ORDER BY nombre ASC")
    lista_pacientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("pacientes.html", pacientes=lista_pacientes)

@app.route("/pacientes/nuevo", methods=["GET", "POST"])
@app.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def guardar_paciente(id=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    paciente = None

    if id:
        cur.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
        paciente = cur.fetchone()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento")
        genero = request.form.get("genero")
        grupo_sanguineo = request.form.get("grupo_sanguineo")
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()
        direccion = request.form.get("direccion", "").strip()
        alergias = request.form.get("alergias", "").strip()

        if not documento:
            flash("Error al registrar: El documento de identidad no puede estar vacío.", "danger")
            cur.close()
            conn.close()
            return render_template("paciente_form.html", paciente=paciente)

        try:
            if id:
                cur.execute("SELECT id FROM pacientes WHERE documento = %s AND id != %s", (documento, id))
            else:
                cur.execute("SELECT id FROM pacientes WHERE documento = %s", (documento,))
            
            existe = cur.fetchone()

            if existe:
                flash("Error al registrar: El documento ya existe.", "danger")
                cur.close()
                conn.close()
                return render_template("paciente_form.html", paciente=paciente)

            if id:
                cur.execute("""
                    UPDATE pacientes 
                    SET nombre=%s, documento=%s, fecha_nacimiento=%s, telefono=%s, 
                        email=%s, direccion=%s, genero=%s, grupo_sanguineo=%s, alergias=%s
                    WHERE id=%s
                """, (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias, id))
                flash("Paciente actualizado exitosamente.", "success")
            else:
                cur.execute("""
                    INSERT INTO pacientes (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, documento, fecha_nacimiento, telefono, email, direccion, genero, grupo_sanguineo, alergias))
                flash("Paciente registrado exitosamente.", "success")

            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("pacientes"))

        except Exception as e:
            conn.rollback()
            flash(f"Error inesperado en la base de datos: {str(e)}", "danger")
            cur.close()
            conn.close()
            return render_template("paciente_form.html", paciente=paciente)

    cur.close()
    conn.close()
    return render_template("paciente_form.html", paciente=paciente)

@app.route("/pacientes/borrar/<int:id>", methods=["POST"])
@login_required
def paciente_borrar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pacientes WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Paciente eliminado", "warning")
    return redirect(url_for("pacientes"))

# ------------------------------------------------------------
# 3. MÓDULO DE MÉDICOS
# ------------------------------------------------------------
@app.route("/medicos")
@login_required
def medicos():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.*, e.nombre AS especialidad_nombre 
        FROM medicos m 
        LEFT JOIN especialidades e ON m.specialty_id = e.id 
        ORDER BY m.nombre ASC
    """)
    lista_medicos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("medicos.html", medicos=lista_medicos)

@app.route("/medico/nuevo", methods=["GET", "POST"])
@login_required
def medico_nuevo():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    # 1. Cargamos las especialidades SIEMPRE
    cur.execute("SELECT * FROM especialidades ORDER BY nombre ASC")
    especialidades = cur.fetchall()
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        numero_licencia = request.form.get("numero_licencia")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        specialty_id = request.form.get("specialty_id")

        try:
            # Asegúrate de usar 'numero_licencia' en lugar de 'documento'
            cur.execute("""
                INSERT INTO medicos (nombre, numero_licencia, telefono, email, specialty_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (nombre, numero_licencia, telefono, email, specialty_id))
            conn.commit()
            flash("Médico registrado exitosamente.", "success")
            cur.close() # Cerramos antes de redirigir
            conn.close()
            return redirect(url_for("medicos")) # <-- RETORNO EN CASO DE ÉXITO
            
        except Exception as e:
            conn.rollback()
            # Esto imprimirá el error técnico real en tu terminal
            print(f"--- ERROR DE MYSQL DETALLADO ---")
            print(f"Error completo: {e}")
            print(f"--------------------------------")
            
            # Cambiamos el mensaje para que sea más específico si es posible
            flash(f"Error al registrar: {str(e)}", "danger")
            
    # Asegúrate de que este render siempre esté al final de la función
    cur.close()
    conn.close()
    return render_template("medico_form.html", medico=None, especialidades=especialidades)

@app.route("/medicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def medico_editar(id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form.get("nombre")
        numero_licencia = request.form.get("numero_licencia")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        specialty_id = request.form.get("specialty_id")

        try:
            cur.execute("""
                UPDATE medicos 
                SET nombre=%s, numero_licencia=%s, telefono=%s, email=%s, specialty_id=%s
                WHERE id=%s
            """, (nombre, numero_licencia, telefono, email, specialty_id, id))
            conn.commit()
            flash("Datos del médico actualizados correctamente.", "success")
            return redirect(url_for("medicos"))
        except Exception as e:
            conn.rollback()
            flash("Error al actualizar: La licencia ya pertenece a otro médico.", "danger")
        finally:
            cur.close()
            conn.close()

    cur.execute("SELECT * FROM medicos WHERE id = %s", (id,))
    medico_actual = cur.fetchone()
    
    cur.execute("SELECT * FROM especialidades ORDER BY nombre ASC")
    especialidades = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template("medico_form.html", medico=medico_actual, especialidades=especialidades)

@app.route("/medicos/borrar/<int:id>", methods=["POST"])
@login_required
def medico_borrar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM medicos WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Médico eliminado del sistema.", "warning")
    return redirect(url_for("medicos"))

# ------------------------------------------------------------
# 4. MÓDULO IMC & NUTRICIÓN (CORREGIDO DE REGISTROS_IMC A IMC_HISTORIAL)
# ------------------------------------------------------------
@app.route("/imc", methods=["GET", "POST"])
@login_required
def imc():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    resultado = None

    if request.method == "POST":
        paciente_id = request.form.get("paciente_id")
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        
        valor_imc = round(peso / (altura ** 2), 2)
        
        if valor_imc < 18.5:
            clasificacion = "Bajo peso"
        elif 18.5 <= valor_imc < 25.0:
            clasificacion = "Normal"
        elif 25.0 <= valor_imc < 30.0:
            clasificacion = "Sobrepeso"
        elif 30.0 <= valor_imc < 35.0:
            clasificacion = "Obesidad I"
        elif 35.0 <= valor_imc < 40.0:
            clasificacion = "Obesidad II"
        else:
            clasificacion = "Obesidad III"

        cur.execute("SELECT recomendacion FROM categorias WHERE nombre = %s", (clasificacion,))
        cat_data = cur.fetchone()
        recomendacion = cat_data["recomendacion"] if cat_data else "Mantener control médico constante."

        try:
            # Corregido: Insertar en la tabla real de tu base de datos 'imc_historial'
            cur.execute("""
                INSERT INTO imc_historial (paciente_id, peso, altura, imc, clasificacion)
                VALUES (%s, %s, %s, %s, %s)
            """, (paciente_id, peso, altura, valor_imc, clasificacion))
            conn.commit()
            
            resultado = {
                "paciente_id": paciente_id,
                "imc": valor_imc,
                "clasificacion": clasificacion,
                "peso": peso,
                "altura": altura,
                "recomendacion": recomendacion
            }
            flash("Cálculo de IMC guardado exitosamente en el historial.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error de base de datos al guardar IMC: {str(e)}", "danger")

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    lista_pacientes = cur.fetchall()
    
    cur.close()
    conn.close()
    # Corregido: Mandar la lista de pacientes con el nombre exacto que espera tu selector en HTML
    return render_template("imc.html", pacientes=lista_pacientes, resultado=resultado)

@app.route("/paciente/<int:paciente_id>/imc/historial")
@login_required
def imc_historial_paciente(paciente_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("SELECT id, nombre FROM pacientes WHERE id = %s", (paciente_id,))
    paciente = cur.fetchone()
    
    if not paciente:
        flash("El paciente especificado no existe.", "danger")
        cur.close()
        conn.close()
        return redirect(url_for("imc"))
        
    cur.execute("""
        SELECT id, peso, altura, imc, clasificacion, fecha 
        FROM imc_historial 
        WHERE paciente_id = %s 
        ORDER BY fecha ASC
    """, (paciente_id,))
    historial_asc = cur.fetchall()
    
    labels = [registro["fecha"].strftime("%d/%m/%Y") if hasattr(registro["fecha"], "strftime") else str(registro["fecha"]) for registro in historial_asc]
    imc_values = [float(registro["imc"]) for registro in historial_asc]
    peso_values = [float(registro["peso"]) for registro in historial_asc]
    
    historial_desc = list(reversed(historial_asc))
    
    cur.close()
    conn.close()
    
    return render_template(
        "imc_historial.html", 
        paciente=paciente, 
        historial=historial_desc,
        labels=labels,
        imc_values=imc_values,      
        peso_values=peso_values     
    )

# ------------------------------------------------------------
# 5. MÓDULO DE MENSAJERÍA / CHAT
# ------------------------------------------------------------
@app.route("/chat", methods=["GET"])
@login_required
def chat_lista():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, username, nombre_completo FROM usuarios WHERE id != %s", (session["user"]["id"],))
    contactos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("chat_lista.html", contactos=contactos)

@app.route("/chat/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def chat_sala(usuario_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    mi_id = session["user"]["id"]

    if request.method == "POST":
        texto = request.form.get("contenido")
        if texto and texto.strip():
            cur.execute("""
                INSERT INTO mensajes (contenido, remitente_id, destinatario_id)
                VALUES (%s, %s, %s)
            """, (texto.strip(), mi_id, usuario_id))
            conn.commit()
            return redirect(url_for("chat_sala", usuario_id=usuario_id))

    cur.execute("UPDATE mensajes SET leido = 1 WHERE remitente_id = %s AND destinatario_id = %s", (usuario_id, mi_id))
    conn.commit()

    cur.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
    receptor = cur.fetchone()

    cur.execute("""
        SELECT * FROM mensajes 
        WHERE (remitente_id = %s AND destinatario_id = %s)
           OR (remitente_id = %s AND destinatario_id = %s)
        ORDER BY fechaEnvio ASC
    """, (mi_id, usuario_id, usuario_id, mi_id))
    mensajes_chat = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("chat.html", receptor=receptor, mensajes_chat=mensajes_chat)

# ------------------------------------------------------------
# 6. MÓDULO DE RECOMENDACIÓN DE ACTIVIDAD FÍSICA
# ------------------------------------------------------------
@app.route("/actividad", methods=["GET", "POST"])
@login_required
def actividad():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    paciente_seleccionado = None
    ultimo_imc = None

    paciente_id = request.args.get("paciente_id") or request.form.get("paciente_id")

    if paciente_id:
        cur.execute("SELECT id, nombre FROM pacientes WHERE id = %s", (paciente_id,))
        paciente_seleccionado = cur.fetchone()

        if paciente_seleccionado:
            cur.execute("""
                SELECT imc, clasificacion FROM imc_historial 
                WHERE paciente_id = %s 
                ORDER BY fecha DESC LIMIT 1
            """, (paciente_id,))
            ultimo_imc = cur.fetchone()

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    lista_pacientes = cur.fetchall()

    cur.close()
    conn.close()
    # Corregido: Pasar la variable 'pacientes' en lugar de lista_pacientes para poblar el select
    return render_template("actividad.html", 
                           pacientes=lista_pacientes, 
                           paciente_seleccionado=paciente_seleccionado, 
                           ultimo_imc=ultimo_imc)

# ------------------------------------------------------------
# 7. MÓDULO DE HISTORIAS CLÍNICAS
# ------------------------------------------------------------
@app.route("/paciente/<int:patient_id>/historias")
@login_required
def historias(patient_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("SELECT id, nombre FROM pacientes WHERE id = %s", (patient_id,))
    paciente = cur.fetchone()
    
    cur.execute("""
        SELECT h.*, u.nombre_completo AS medico_nombre 
        FROM historias_clinicas h
        LEFT JOIN usuarios u ON h.medico_id = u.id
        WHERE h.paciente_id = %s ORDER BY h.fecha DESC
    """, (patient_id,))
    lista_historias = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template("historias.html", paciente=paciente, historias=lista_historias)

@app.route("/paciente/<int:patient_id>/historia/nueva", methods=["GET", "POST"])
@login_required
def historia_nueva(patient_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == "POST":
        medico_id = session["user"]["id"]
        tipo = request.form.get("tipo")
        nota = request.form.get("nota")

        cur.execute("""
            INSERT INTO historias_clinicas (paciente_id, medico_id, tipo, nota)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, medico_id, tipo, nota))
        conn.commit()
        flash("Observación clínica registrada en la historia.", "success")
        cur.close()
        conn.close()
        return redirect(url_for("historias", patient_id=patient_id))

    cur.close()
    conn.close()
    return render_template("historia_form.html", paciente_id=patient_id)

# ------------------------------------------------------------
# 8. MÓDULO DE CITAS MÉDICAS
# ------------------------------------------------------------
@app.route("/citas")
@login_required
def citas():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.*, p.nombre AS paciente_nombre, m.nombre AS medico_nombre
        FROM citas c
        JOIN pacientes p ON c.paciente_id = p.id
        JOIN medicos m ON c.medico_id = m.id
        ORDER BY c.fecha DESC, c.hora DESC
    """)
    lista_citas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("citas.html", citas=lista_citas)

@app.route("/citas/nueva", methods=["GET", "POST"])
@login_required
def cita_nueva():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if request.method == "POST":
        paciente_id = request.form.get("paciente_id")
        medico_id = request.form.get("medico_id")
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        motivo = request.form.get("motivo")

        try:
            cur.execute("""
                INSERT INTO citas (paciente_id, medico_id, fecha, hora, motivo)
                VALUES (%s, %s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, hora, motivo))
            conn.commit()
            flash("Cita médica agendada correctamente.", "success")
            return redirect(url_for("citas"))
        except Exception as e:
            conn.rollback()
            flash("Error al agendar la cita. Verifique los datos correspondientes.", "danger")
        finally:
            cur.close()
            conn.close()

    cur.execute("SELECT id, nombre FROM pacientes ORDER BY nombre ASC")
    pacientes = cur.fetchall()
    
    cur.execute("SELECT id, nombre FROM medicos ORDER BY nombre ASC")
    medicos_lista = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template("cita_form.html", cita=None, pacientes=pacientes, medicos=medicos_lista)


from werkzeug.security import generate_password_hash
from db import get_connection

def registrar_medico():
    conn = get_connection()
    cur = conn.cursor()

    # La contraseña que quieres (123456789) la convertimos en hash seguro
    password_segura = generate_password_hash("123456789")

    try:
        cur.execute("""
            INSERT INTO usuarios (username, password_hash, nombre_completo, role_id) 
            VALUES (%s, %s, %s, 2)
        """, ("drjhonatan", password_segura, "Dr. Jhonatan"))
        conn.commit()
        print("¡Éxito! El usuario 'drjhonatan' ha sido creado correctamente.")
    except Exception as e:
        print(f"Hubo un error (quizás el usuario ya existe): {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    registrar_medico()


@app.route("/citas/borrar/<int:id>", methods=["POST"])
@login_required
def cita_borrar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM citas WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Cita médica cancelada.", "warning")
    return redirect(url_for("citas"))

@app.route("/citas/cambiar_estado/<int:id>", methods=["POST"])
@login_required
def cita_cambiar_estado(id):
    nuevo_estado = request.form.get("estado")
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE citas 
            SET estado = %s 
            WHERE id = %s
        """, (nuevo_estado, id))
        conn.commit()
        flash(f"Estado de la cita actualizado a '{nuevo_estado}'.", "success")
    except Exception as e:
        conn.rollback()
        flash("Error al cambiar el estado de la cita.", "danger")
    finally:
        cur.close()
        conn.close()
        
    return redirect(url_for("citas"))

# ------------------------------------------------------------
# COMANDO AUXILIAR PARA GENERAR EL ADMIN POR DEFECTO
# ------------------------------------------------------------
@app.route("/init_admin")
def init_admin():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("INSERT IGNORE INTO roles (id, nombre) VALUES (1, 'admin'), (2, 'medico')")
    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM usuarios")
    if cur.fetchone()["c"] > 0:
        cur.close()
        conn.close()
        return "El sistema ya cuenta con usuarios creados."

    pw = generate_password_hash("admin123")
    cur.execute("""
        INSERT INTO usuarios (username, password_hash, nombre_completo, role_id)
        VALUES (%s, %s, %s, 1)
    """, ("admin", pw, "Administrador Sistema",))
    conn.commit()
    
    cur.close()
    conn.close()
    return "Usuario 'admin' inicializado con éxito."

if __name__ == "__main__":
    app.run(debug=True)