# Crea un archivo llamado 'fix_login.py' y ejecútalo con: python fix_login.py
from werkzeug.security import generate_password_hash
from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Actualizamos la contraseña a '123456789' para dr.jhon
nueva_pass = generate_password_hash("123456789")
cur.execute("UPDATE usuarios SET password_hash = %s WHERE username = 'dr.jhon'", (nueva_pass,))

conn.commit()
cur.close()
conn.close()
print("¡Contraseña de dr.jhon actualizada exitosamente!")