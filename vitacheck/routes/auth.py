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
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))

        if user['estado'] == 'pendiente':
            flash('Tu cuenta está pendiente de aprobación.', 'warning')
            return redirect(url_for('auth.login'))

        if user['estado'] == 'rechazado':
            flash('Tu cuenta ha sido rechazada. Contacta al administrador.', 'danger')
            return redirect(url_for('auth.login'))

        session['user'] = user
        return redirect(url_for('auth.dashboard'))

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


@auth_bp.route("/init_admin")
def init_admin():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("INSERT IGNORE INTO roles (id, nombre) VALUES (1, 'admin'), (2, 'medico')")
    conn.commit()
    cur.execute("SELECT COUNT(*) as c FROM usuarios")
    if cur.fetchone()["c"] > 0:
        cur.close(); conn.close()
        return "El sistema ya cuenta con usuarios."
    cur.execute("""
        INSERT INTO usuarios (username, password_hash, nombre_completo, role_id)
        VALUES (%s, %s, %s, 1)
    """, ("admin", generate_password_hash("admin123"), "Administrador Sistema"))
    conn.commit()
    cur.close(); conn.close()
    return "Admin creado exitosamente."
