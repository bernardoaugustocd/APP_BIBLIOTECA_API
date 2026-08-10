from flask import Blueprint, jsonify, request, abort

from conectar.funcaoConectar import conectar

serie_B_bp = Blueprint('SerieB', __name__)

#ROTAS PARA A TABELA SerieB
##ROTA GET
##############################################
@serie_B_bp.route("/SerieB", methods=["GET"])
def listar_CadastrosB():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idSerieB, NomeClube, PontosClube, JogosClube, SaldoGols, VitoriasClube, DerrotasClube, EmpateClube, PosicaoTabela FROM SerieB")
    dados = [
        {"idSerieB": row[0], "NomeClube": row[1], "PontosClube": row[2], "JogosClube": row[3], "SaldoGols": row[4], "VitoriasClube": row[5], "DerrotasClube": row[6], "EmpateClube": row[7], "PosicaoTabela": row[8]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################
@serie_B_bp.route("/SerieB", methods=["POST"])
def criar_usuarioB():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeClube", "PontosClube", "JogosClube", "SaldoGols", "VitoriasClube", "DerrotasClube", "EmpateClube", "PosicaoTabela"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO SerieB (NomeClube, PontosClube, JogosClube, SaldoGols, VitoriasClube, DerrotasClube, EmpateClube, PosicaoTabela)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (dados["NomeClube"], dados["PontosClube"], dados["JogosClube"], dados["SaldoGols"], dados["VitoriasClube"], dados["DerrotasClube"], dados["EmpateClube"], dados["PosicaoTabela"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idSerieB": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/SerieB/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@serie_B_bp.route("/SerieB/<int:idSerieB>", methods=["PUT", "PATCH"])
def atualizar_usuarioB(idSerieB):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeClube", "PontosClube", "JogosClube", "SaldoGols", "VitoriasClube", "DerrotasClube", "EmpateClube", "PosicaoTabela"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeClube", "PontosClube", "JogosClube", "SaldoGols", "VitoriasClube", "DerrotasClube", "EmpateClube", "PosicaoTabela"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerieB)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE SerieB SET {', '.join(set_clauses)} WHERE idSerieB = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


##ROTA DELETE
#############################################
@serie_B_bp.route("/SerieB/<int:idSerieB>", methods=["DELETE"])
def deletar_usuarioB(idSerieB):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM SerieB WHERE idSerieB = ?", (idSerieB,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)