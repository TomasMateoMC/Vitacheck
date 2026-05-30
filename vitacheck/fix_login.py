# Crea un archivo llamado 'fix_login.py' y ejecútalo con: python fix_login.py
from werkzeug.security import generate_password_hash
from db import get_connection

conn = get_connection()
cur = conn.cursor()

# Actualizamos la contraseña a '123456789' para dr.carlos
nueva_pass = generate_password_hash("1234")
cur.execute("UPDATE usuarios SET password_hash = %s WHERE username = 'dr.carlos'", (nueva_pass,))

conn.commit()
cur.close()
conn.close()
print("¡Contraseña de dr.carlos actualizada exitosamente!")