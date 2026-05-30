from flask import Flask
from routes.auth      import auth_bp
from routes.pacientes import pacientes_bp
from routes.medicos   import medicos_bp
from routes.citas     import citas_bp
from routes.historias import historias_bp
from routes.imc       import imc_bp
from routes.chat      import chat_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "mi_clave_secreta_123")

app.register_blueprint(auth_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(citas_bp)
app.register_blueprint(historias_bp)
app.register_blueprint(imc_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
