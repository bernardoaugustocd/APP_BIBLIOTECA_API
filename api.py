from flask import Flask, jsonify

from conectar.funcaoConectar import conectar

from endpoints.aluno import aluno
from endpoints.emprestimos import emprestimos
from endpoints.funcionarios import funcionarios
from endpoints.livros import livros

app = Flask(__name__)

app.register_blueprint(aluno)
app.register_blueprint(emprestimos)
app.register_blueprint(funcionarios)
app.register_blueprint(livros)

if __name__ == "__main__":
    app.run(debug=True)