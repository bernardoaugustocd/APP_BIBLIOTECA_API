from flask import Flask, jsonify

from conectar.funcaoConectar import conectar

from endpoints.serieA import serie_A_bp
from endpoints.serieB import serie_B_bp
from endpoints.serieC import serie_C_bp
from endpoints.serieD import serie_D_bp

app = Flask(__name__)

app.register_blueprint(serie_A_bp)
app.register_blueprint(serie_B_bp)
app.register_blueprint(serie_C_bp)
app.register_blueprint(serie_D_bp)

if __name__ == "__main__":
    app.run(debug=True)