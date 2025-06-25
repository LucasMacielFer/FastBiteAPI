from flask import Blueprint, jsonify, request, send_from_directory
from app.models import *

api_bp = Blueprint('api', __name__)

@api_bp.route("/login", methods=["POST"])
def verificacao_login():
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    user = dados.get('user')
    password = dados.get('password')
    if not user or not password:
        return jsonify({"msg": "Usuário ou senha ausentes"}), 400
    
    info = {}
    if verifica_login(user, password):
        info["msg"] = "Acesso concedido"
        return jsonify(info), 200
    else:
        info["msg"] = "Acesso negado"
        return jsonify(info), 401
    
@api_bp.route("/mesas/<int:mesa>", methods=["POST"])
def registro_mesa(mesa):
    if not mesa:
        return jsonify({"msg": "mesa ausente"}), 400

    if registra_mesa(mesa):
        return jsonify({"msg":"Sucesso"}), 201
    else:
        return jsonify({"msg":"Falha no registro"}), 405
    
@api_bp.route("/mesas/<int:mesa>", methods=["DELETE"])
def remocao_mesa(mesa):
    if not mesa:
        return jsonify({"msg": "mesa ausente"}), 400
    
    if remove_mesa(mesa):
        return jsonify({"msg":"Sucesso"}), 204
    else:
        return jsonify({"msg":"Falha na remoção"}), 405
    
@api_bp.route("/cardapio/visualizar/comidas", methods=["GET"])
def solicitacao_comidas():
    cardapio = {}
    itensCardapio = solicita_cardapio(True)
    if itensCardapio:
        for item in itensCardapio:
            itemNo = item["IDitem"]
            cardapio[itemNo] = item

    return jsonify(cardapio), 200

@api_bp.route("/cardapio/visualizar/bebidas", methods=["GET"])
def solicitacao_bebidas():
    cardapio = {}
    itensCardapio = solicita_cardapio(False)
    if itensCardapio:
        for item in itensCardapio:
            itemNo = item["IDitem"]
            cardapio[itemNo] = item

    return jsonify(cardapio), 200
    
@api_bp.route("/cardapio/adicionar/comida", methods=["POST"])
def adicao_cardapio_c():
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    nome = dados.get('nome')
    desc = dados.get('descricao')
    preco = dados.get('preco')
    ext = dados.get('extensao')
    ehComida = True

    if not nome or not desc or not preco:
        return jsonify({"msg": "Algum dado ausente"}), 400
    
    infos = {"nome":nome, "descricao":desc, "preco":preco, "extensao":ext, "ehComida":ehComida}

    if insere_cardapio(infos):
        return jsonify({"msg":  "Sucesso"}), 201
    else:
        return jsonify({"msg":  "Falha na inserção"}), 409
    
@api_bp.route("/cardapio/adicionar/bebida", methods=["POST"])
def adicao_cardapio_b():
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    nome = dados.get('nome')
    desc = dados.get('descricao')
    preco = dados.get('preco')
    ext = dados.get('extensao')
    ehComida = False

    if not nome or not desc or not preco:
        return jsonify({"msg": "Algum dado ausente"}), 400
    
    infos = {"nome":nome, "descricao":desc, "preco":preco, "extensao":ext, "ehComida":ehComida}

    if insere_cardapio(infos):
        return jsonify({"msg":  "Sucesso"}), 201
    else:
        return jsonify({"msg":  "Falha na inserção"}), 409
    
@api_bp.route("/cardapio/<int:IDitem>", methods=["DELETE"])
def remocao_cardapio(IDitem): 
    if not IDitem:
        return jsonify({"msg": "IDitem ausente"}), 400

    if remove_cardapio(IDitem):
        return jsonify({"msg":  "Sucesso"}), 204
    else:
        return jsonify({"msg":  "Falha na remoção"}), 405
    
@api_bp.route("/cardapio/modificar", methods=["POST"])
def alteracao_cardapio():
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    
    itemNo = dados.get("IDitem")
    campo = dados.get("campo")
    valor = dados.get("valor")

    if not itemNo or not campo or not valor:
        return jsonify({"msg": "Algum dado ausente"}), 400
    
    # Se tentar editar a figura...
    if campo == "figura" or campo == "extensao":
        try:
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], f"newFig.{valor}")
            with open(caminho, 'rb') as file:
                valor = file.read()
        except:
            valor = None

    if altera_info_cardapio(itemNo, campo, valor):
        return jsonify({"msg":  "Sucesso"}), 200
    else:
        return jsonify({"msg":  "Falha na alteração"}), 405
    
@api_bp.route("/pedidos/criar", methods=["POST"])
def criacao_pedido():
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    
    mesa = dados.get("IDmesa")
    relacaoItens = dados.get("itens")

    if not mesa or not relacaoItens:
        return jsonify({"msg": "Algum dado ausente"}), 400

    numPedido = cria_pedido(mesa, relacaoItens)
    if numPedido > -1:
        return jsonify({"numPedido":  numPedido}), 201
    else:
        return jsonify({"numPedido":  numPedido}), 405
    
@api_bp.route("/pedidos/<int:IDpedido>/entregar", methods=["POST"])
def entrega_de_pedido(IDpedido):
    if not IDpedido:
        return jsonify({"msg": "IDpedido ausente"}), 400

    if entrega_pedido(IDpedido):
        return jsonify({"msg":  "Sucesso"}), 200
    else:
        return jsonify({"msg":  "Falha na mudança de status do pedido"}), 405
    
@api_bp.route("/pedidos/<int:IDpedido>", methods=["DELETE"])
def cancelamento_pedido(IDpedido):
    if not IDpedido:
        return jsonify({"msg": "IDpedido ausente"}), 400

    if cancela_pedido(IDpedido):
        return jsonify({"msg":  "Sucesso"}), 204
    else:
        return jsonify({"msg":  "Falha na mudança de status do pedido"}), 405
    
@api_bp.route("/mesas/<int:mesa>", methods=["GET"])
def consulta_mesa(mesa):
    retorno = {}
    if not mesa:
        return jsonify({"msg": "mesa ausente"}), 400
    
    itensComanda = consulta_consumo(mesa)
    if itensComanda:
        i = 0
        for item in itensComanda:
            retorno[f"{i}"] = item
            i += 1
    if retorno != {}:
        return jsonify(retorno), 200
    else:
        return jsonify({"msg":  "Falha na consulta"}), 405
    
@api_bp.route("/consulta/cozinha", methods=["GET"])
def consulta_cozinha():
    retorno = {}
    fila = consulta_ativos()

    if fila:
        i = 0
        for item in fila:
            retorno[f"{i}"] = item
            i += 1

    if retorno != {}:
        return jsonify(retorno), 200
    else:
        return jsonify({"msg":  "Falha na consulta"}), 405
    
@api_bp.route("/pedidos/<int:IDpedido>/editar", methods=["POST"])
def editar_consumo(IDpedido):
    dados = request.get_json()
    if not dados:
        return jsonify({"msg": "Nenhum dado enviado"}), 400
    
    IDitem = dados.get("IDitem")
    novaQtd = dados.get("quantidade")
    if not IDitem or not novaQtd or not IDpedido:
        return jsonify({"msg": "Algum dado ausente"}), 400
    
    if altera_consumo(IDpedido, IDitem, novaQtd):
        return jsonify({"msg":  "Sucesso"}), 200
    else:
        return jsonify({"msg":  "Falha na alteração"}), 405

@api_bp.route("/mesas/<int:mesa>/fechar", methods=["POST"])
def fechar_mesa(mesa):
    if not mesa:
        return jsonify({"msg": "mesa ausente"}), 400
    
    if fecha_comanda(mesa):
        return jsonify({"msg":"Sucesso"}), 204
    else:
        return jsonify({"msg":"Falha no fechamento de comanda"}), 405
    
@api_bp.route("/historico", methods=["GET"])
def verificar_historico():
    retorno = {}
    historico = consulta_historico_mensal()

    if historico:
        i = 0
        for item in historico:
            retorno[f"{i}"] = item
            i += 1

    return jsonify(retorno), 200

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload_imagem():
    if 'imagem' not in request.files:
        return jsonify({"erro": "Nenhum campo de arquivo 'imagem' foi enviado."}), 400

    file = request.files['imagem']
    if file.filename == '':
        return jsonify({"erro": "Nenhuma imagem selecionada."}), 400

    if file and allowed_file(file.filename):
        try:
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"newFig.{file.filename.rsplit('.', 1)[1].lower()}")
            file.save(save_path)
            return jsonify({"mensagem": f"Arquivo salvo com sucesso."}), 201
        except Exception as e:
            return jsonify({"erro": f"Não foi possível salvar o arquivo: {e}"}), 500
    else:
        return jsonify({"erro": "Tipo de arquivo não permitido."}), 400
    
@api_bp.route('/imagem/<path:filename>', methods=["GET"])
def download_imagem(filename):
    return send_from_directory(
            current_app.config['MENU_IMAGES'],
            filename,
            as_attachment=True
        )