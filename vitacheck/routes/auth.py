from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection
from decorators import login_required, admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
         SELECT u.*, r.nombre as rol 
         FROM usuarios u 
         JOIN roles r ON u.role_id = r.id 
         WHERE u.username = %s
         """, (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        # 1. Validación de usuario y contraseña
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))

        # 2. Validación de estado (seguridad)
        estado = user.get('estado', 'pendiente') 
        if estado == 'pendiente':
            flash('Tu cuenta está pendiente de aprobación.', 'warning')
            return redirect(url_for('auth.login'))

        if estado == 'rechazado':
            flash('Tu cuenta ha sido rechazada.', 'danger')
            return redirect(url_for('auth.login'))
        
        # 3. Guardar la sesión y redireccionar según el ROL
        # Esto solo se ejecuta si el usuario es válido y está aprobado
        session['user'] = user 
        
        if user['rol'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user['rol'] == 'medico': # O 'especialista' según tu DB
            return redirect(url_for('medicos.dashboard'))
        else:
            return redirect(url_for('pacientes.dashboard'))
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre_completo  = request.form['nombre_completo']
        username         = request.form['username']
        password         = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("""
                INSERT INTO usuarios (username, password_hash, nombre_completo, role_id, estado)
                VALUES (%s, %s, %s, 2, 'pendiente')
            """, (username, generate_password_hash(password), nombre_completo))
            conn.commit()
            cur.close()
            conn.close()
            flash('Cuenta creada. Espera aprobación del administrador.', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/")
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@auth_bp.route('/solicitudes')
@login_required
@admin_required
def solicitudes():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE estado = 'pendiente' ORDER BY created_at DESC")
    pendientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('solicitudes.html', pendientes=pendientes)


@auth_bp.route('/solicitudes/<int:user_id>/<accion>')
@login_required
@admin_required
def gestionar_solicitud(user_id, accion):
    if accion not in ('activo', 'rechazado'):
        return redirect(url_for('auth.solicitudes'))

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("UPDATE usuarios SET estado = %s WHERE id = %s", (accion, user_id))
    conn.commit()
    cur.close()
    conn.close()

    flash('Usuario aprobado.' if accion == 'activo' else 'Usuario rechazado.',
          'success' if accion == 'activo' else 'danger')
    return redirect(url_for('auth.solicitudes'))

