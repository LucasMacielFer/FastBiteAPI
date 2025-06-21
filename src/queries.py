from DB_connect import send_query, insert_delete, insert_and_get_ID
from datetime import date, datetime

# Para verificar login e senha
def verifica_login(conn, user=str, password=str):
    query = f"select * from users where user=%s and password=%s;"
    loginInfo = send_query(conn, query, (user, password))
    loginInfo = loginInfo[0]
    if loginInfo == []:
        return False
    else: 
        return True
    
# Para inserir uma mesa no sistema
def registra_mesa(conn, IDmesa=int):
    query = f"select * from mesas where IDmesa=%s;"
    mesaRegistrada = send_query(conn, query, (IDmesa,))
    mesaRegistrada = mesaRegistrada[0]
    if mesaRegistrada == []:
        insert_delete(conn, f"insert into mesas values (%s);", (IDmesa,))
        return True
    else:
        return False
    
# Para remover uma mesa do sistema
def remove_mesa(conn, IDmesa=int):
    query = f"select * from mesas where IDmesa=%s;"
    mesaRegistrada = send_query(conn, query, (IDmesa,))
    mesaRegistrada = mesaRegistrada[0]
    if mesaRegistrada != []:
        if insert_delete(conn, f"delete from mesas where IDmesa=%s;", (IDmesa,)):
            return True
    return False

# Acessa o cardápio. comida = True -> comidas, comida = False -> bebidas
def solicita_cardapio(conn, comida=bool):
    cardapio = []
    if comida:
        query = "select * from cardapio where ehComida=1;"
    else:
        query = "select * from cardapio where ehComida=0;"
    listagem = send_query(conn, query, [])
    listagem = listagem[0]
    for p in listagem:
        produto = {}
        produto["IDitem"] = p[0]
        produto["nome"] = p[1]
        produto["descricao"] = p[2]
        produto["preco"] = p[3]
        produto["figura"] = None
        if p[4] != None:
            caminho = f"img/figItem{p[0]}.{p[5]}"
            with open(caminho, 'wb') as file:
                file.write(p[4])
            produto["figura"] = caminho

        cardapio.append(produto)
    return cardapio

# Insere item novo no cardápio
# Recebe um dicionário com os seguintes itens:
# "nome" -> nome
# "descricao" -> descrição
# "preco" -> preço
# "extensao" -> Extensão do arquivo, ou None
# "ehComida" -> Booleano: è comida ou bebida?
def insere_cardapio(conn, informacoes):
    nome = informacoes["nome"]
    descricao = informacoes["descricao"]
    preco = informacoes["preco"]
    extensao = informacoes["extensao"]
    ehComida = informacoes["ehComida"]

    query = f"select nome from cardapio where nome=%s;"
    itemRegistrado = send_query(conn, query, (nome,))
    itemRegistrado = itemRegistrado[0]
    if itemRegistrado != []:
        return False
    
    query = "insert into cardapio (nome, descricao, preco, figura, extensao, ehComida) values (%s, %s, %s, %s, %s, %s)"

    if extensao:
        try:
            caminho = f"img/figAdd.{extensao}"
            with open(caminho, 'rb') as file:
                figBin = file.read()
        except:
            print("Failed to open file.")
            figBin = None
    else:
        figBin = None

    if insert_delete(conn, query, (nome, descricao, preco, figBin, extensao, ehComida)):
        return True
    else:
        return False
    
# Função para remover algum item do cardápio
def remove_cardapio(conn, idItem=int):
    query = f"select idItem from cardapio where idItem=%s;"
    mesaRegistrada = send_query(conn, query, (idItem,))
    mesaRegistrada = mesaRegistrada[0]
    if mesaRegistrada != []:
        if insert_delete(conn, f"delete from cardapio where idItem=%s;", (idItem,)):
            return True
    return False

# Função para modificar o preço de algum item do cardápio
def altera_info_cardapio(conn, idItem, campo, novoValor):
    query = f"select idItem from cardapio where idItem=%s;"
    mesaRegistrada = send_query(conn, query, (idItem,))
    mesaRegistrada = mesaRegistrada[0]
    if mesaRegistrada != []:
        if insert_delete(conn, f"update cardapio set {campo}=%s where idItem=%s;", (novoValor, idItem)):
            return True
    return False

# Criação de pedido - utilizado pela interface das mesas
# "listaItens" é um conjunto de tuplas do tipo (idItem, quantidade)
# Retorna o número do pedido
def cria_pedido(conn, mesa, listaItens):
    data = date.today()
    hora = datetime.now().time()
    query = f"select * from mesas where IDmesa=%s;"
    mesaRegistrada = send_query(conn, query, (mesa,))
    mesaRegistrada = mesaRegistrada[0]

    if listaItens == [] or mesaRegistrada == []:
        return -1
    
    for i in listaItens:
        query = f"select IDitem from cardapio where IDitem=%s;"
        itemRegistrado = send_query(conn, query, (i[0],))
        itemRegistrado = itemRegistrado[0]
        if itemRegistrado == []:
            return -1

    pedidoID = insert_and_get_ID(conn, "insert into pedido (IDmesa, data, hora) values (%s, %s, %s);", (mesa, data, hora))
    if pedidoID != -1:
        for i in listaItens:
            insert_delete(conn, "insert into itens_pedido (IDpedido, IDitem, quantidade) values (%s, %s, %s)", (pedidoID, i[0], i[1]))
        insert_delete(conn, "insert into pedidos_ativos (IDpedido, status) values (%s, %s)", (pedidoID, "Em preparo"))

    return pedidoID

# "Entrega" de pedido - Utilizado pela interface da cozinha
def entrega_pedido(conn, IDpedido):
    query = f"select IDpedido from pedidos_ativos where IDpedido=%s;"
    pedidoRegistrado = send_query(conn, query, (IDpedido,))
    pedidoRegistrado = pedidoRegistrado[0]

    if pedidoRegistrado == []:
        return False

    return insert_delete(conn, "update pedidos_ativos set status=\"Entregue\" where IDpedido=%s",(IDpedido,))

# Cancelamento de pedido - Utilizado pela interface da cozinha ou pela interface do caixa
def cancela_pedido(conn, IDpedido):
    query = f"select IDpedido from pedidos_ativos where IDpedido=%s;"
    pedidoRegistrado = send_query(conn, query, (IDpedido,))
    pedidoRegistrado = pedidoRegistrado[0]

    if pedidoRegistrado == []:
        return False

    deletion = insert_delete(conn, "delete from pedidos_ativos where IDpedido=%s",(IDpedido,))
    insertion = insert_delete(conn, "insert into pedidos_historico (IDpedido, status) values (%s, %s)",(IDpedido, "Cancelado"))
    return deletion and insertion

# Consulta de comanda pela interface do caixa
def consulta_consumo(conn, IDmesa):
    query = f"select * from mesas where IDmesa=%s;"
    mesaRegistrada = send_query(conn, query, (IDmesa,))
    mesaRegistrada = mesaRegistrada[0]
    
    if mesaRegistrada == []:
        return []
    
    query = "select p.IDpedido, data, hora, c.IDitem, c.nome, preco, quantidade from pedido p join pedidos_ativos pa on p.IDpedido=pa.IDpedido join itens_pedido ip on p.IDpedido = ip.IDpedido join cardapio c on c.IDitem = ip.IDitem where p.IDmesa = %s and pa.status = \"Entregue\""
    consumo = send_query(conn, query, (IDmesa,))
    consumo = consumo[0]
    return consumo

# Mudança de quantidade de um item pelo caixa
# O stored procedure deleta o registro caso a quantidade seja zero. No worries! :)
def altera_consumo(conn, IDpedido, IDitem, novaQtd):
    query = f"select pa.IDpedido from pedidos_ativos pa join itens_pedido ip on pa.IDpedido = ip.IDpedido where pa.IDpedido=%s and ip.IDitem=%s;"
    pedidoRegistrado = send_query(conn, query, (IDpedido,IDitem))
    pedidoRegistrado = pedidoRegistrado[0]
    
    if pedidoRegistrado == []:
        return False
    
    spCall = "CALL sp_atualiza_item_pedido(%s, %s, %s);"
    return insert_delete(conn, spCall, (IDpedido,IDitem, novaQtd))

def fecha_comanda(conn, IDmesa):
    query = f"select * from mesas where IDmesa=%s;"
    mesaRegistrada = send_query(conn, query, (IDmesa,))
    mesaRegistrada = mesaRegistrada[0]

    if mesaRegistrada == []:
        return False

    pedidos_ativos_entregues = send_query(conn, "select pa.IDpedido from pedidos_ativos pa join pedido p on pa.IDpedido = p.IDpedido where IDmesa = %s and pa.status = \"Entregue\"", (IDmesa,))
    pedidos_ativos_nao_entregues = send_query(conn, "select pa.IDpedido from pedidos_ativos pa join pedido p on pa.IDpedido = p.IDpedido where IDmesa = %s and pa.status = \"Em preparo\"", (IDmesa,))
    pedidos_ativos_entregues = pedidos_ativos_entregues[0]
    pedidos_ativos_nao_entregues = pedidos_ativos_nao_entregues[0]

    if pedidos_ativos_entregues != []:
        for p in pedidos_ativos_entregues:
            insert_delete(conn, "insert into pedidos_historico (IDpedido, status) values (%s, %s)", (p[0],"Finalizado"))
            insert_delete(conn, "delete from pedidos_ativos where IDpedido=%s", (p[0],))


    if pedidos_ativos_nao_entregues != []:
        for p in pedidos_ativos_nao_entregues:
            insert_delete(conn, "insert into pedidos_historico (IDpedido, status) values (%s, %s)", (p[0],"Cancelado"))
            insert_delete(conn, "delete from pedidos_ativos where IDpedido=%s", (p[0],))

    return True

# Query de consulta ao histórico mensal
# O BD possui um event para manter os registros atualizados apenas para o mês vigente (regime D-1)
def consulta_historico_mensal(conn):
    query = "select p.IDpedido, p.IDmesa, p.data, p.hora, ip.IDitem, ip.quantidade, ph.status from pedido p natural join itens_pedido ip natural join pedidos_historico ph order by p.IDpedido"
    historico = send_query(conn, query, [])
    historico = historico[0]
    return historico