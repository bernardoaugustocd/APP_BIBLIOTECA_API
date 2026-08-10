from flask import Blueprint, jsonify, request, abort

from conectar.funcaoConectar import conectar

serie_A_bp = Blueprint('SerieA', __name__)

#ROTAS PARA A TABELA SerieA
##ROTA GET
##############################################
@serie_A_bp.route("/SerieA", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idSerieA, NomeClube, PontosClube, JogosClube, SaldoGols, VitoriasClube, DerrotasClube, EmpateClube, PosicaoTabela FROM SerieA")
    dados = [
        {"idSerieA": row[0], "NomeClube": row[1], "PontosClube": row[2], "JogosClube": row[3], "SaldoGols": row[4], "VitoriasClube": row[5], "DerrotasClube": row[6], "EmpateClube": row[7], "PosicaoTabela": row[8]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

@serie_A_bp.route("/SerieA", methods=["POST"])
def criar_usuario():
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
        "INSERT INTO SerieA (NomeClube, PontosClube, JogosClube, SaldoGols, VitoriasClube, DerrotasClube, EmpateClube, PosicaoTabela)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (dados["NomeClube"], dados["PontosClube"], dados["JogosClube"], dados["SaldoGols"], dados["VitoriasClube"], dados["DerrotasClube"], dados["EmpateClube"], dados["PosicaoTabela"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idSerieA": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/SerieA/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@serie_A_bp.route("/SerieA/<int:idSerieA>", methods=["PUT", "PATCH"])
def atualizar_usuario(idSerieA):
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

    valores.append(idSerieA)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE SerieA SET {', '.join(set_clauses)} WHERE idSerieA = ?",
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
@serie_A_bp.route("/SerieA/<int:idSerieA>", methods=["DELETE"])
def deletar_usuario(idSerieA):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM SerieA WHERE idSerieA = ?", (idSerieA,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)