from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection
from decorators import login_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat")
@login_required
def chat_lista():
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id, username, nombre_completo FROM usuarios WHERE id!=%s", (session["user"]["id"],))
    contactos = cur.fetchall()
    cur.close(); conn.close()
    return render_template("chat_lista.html", contactos=contactos)


@chat_bp.route("/chat/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def chat_sala(usuario_id):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    mi_id = session["user"]["id"]

    if request.method == "POST":
        texto = request.form.get("contenido", "").strip()
        if texto:
            cur.execute("""
                INSERT INTO mensajes (contenido, remitente_id, destinatario_id)
                VALUES (%s,%s,%s)
            """, (texto, mi_id, usuario_id))
            conn.commit()
            cur.close(); conn.close()
            return redirect(url_for("chat.chat_sala", usuario_id=usuario_id))

    cur.execute("UPDATE mensajes SET leido=1 WHERE remitente_id=%s AND destinatario_id=%s", (usuario_id, mi_id))
    conn.commit()

    cur.execute("SELECT id, nombre_completo FROM usuarios WHERE id=%s", (usuario_id,))
    receptor = cur.fetchone()

    cur.execute("""
        SELECT * FROM mensajes
        WHERE (remitente_id=%s AND destinatario_id=%s)
           OR (remitente_id=%s AND destinatario_id=%s)
        ORDER BY fechaEnvio ASC
    """, (mi_id, usuario_id, usuario_id, mi_id))
    mensajes = cur.fetchall()
    cur.close(); conn.close()
    return render_template("chat.html", receptor=receptor, mensajes_chat=mensajes)
