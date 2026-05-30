from flask import Blueprint, render_template, redirect, url_for, flash
from db import get_connection
from decorators import login_required, admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin/dashboard")
@login_required
@admin_required
def dashboard():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    
    # Listar usuarios pendientes de aprobación
    cur.execute("SELECT * FROM usuarios WHERE estado = 'pendiente' ORDER BY created_at DESC")
    pendientes = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template("admin_dashboard.html", pendientes=pendientes)