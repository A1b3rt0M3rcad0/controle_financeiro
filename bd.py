import mysql.connector
import pandas as pd
import numpy as np



def cnx():
    USER = 'usuario'
    PASSWORD = 'usuario'
    HOST = 'localhost'
    DATABASE = 'financa_pessoal'
    # Cria a conexão com o banco de dados
    cnx = mysql.connector.connect(
        user=USER, 
        password=PASSWORD, 
        host= HOST, 
        database= DATABASE)
    return cnx


def valida_usuario(cnx, username, password):
    with cnx.cursor() as cursor:
        # Executa a procedure
        query = f'CALL validaUsuario("{username}", "{password}")'
        cursor.execute(query)
        resultado = cursor.fetchall()
        # cria um data frame para consulta
        df = pd.DataFrame(resultado)
        # Fecha o cursor e a conexão
        cursor.close()
        cnx.close()
        # retorna o valor do dataframe        
        return df.iloc[0][0]

def ver_dica_password(cnx, username):
    with cnx.cursor() as cursor:
        # executa a procedure
        query = f"CALL verDicaPassword('{username}')"
        cursor.execute(query)
        resultado = cursor.fetchall()
        try:
            # cria um data framepara consultar
            df = pd.DataFrame(resultado)
            # fecha a conexao e o cursor
            cnx.close()
            if df.iloc[0][0] == 0:
                return 'Username not exists'
            else:
                return df.iloc[0][0]
        except:
            return 'Error: bd.ver_dica_password()'


def criar_conta(cnx, username, password, password_hint):
    if len(username) > 50 or len(password) > 50 or len(password_hint) > 100:
        return 'One of the information is too long'
    elif len(username) < 6 or len(password) < 6 or len(password_hint) < 6:
        return 'One of the information is too short'
    else:
        cursor = cnx.cursor()
        # Chama a procedure "criarUsuario"
        cursor.callproc("criarUsuario", (username, password, password_hint))
        # Lê o resultado da procedure
        result = next(cursor.stored_results())
        rows = result.fetchall()
        # Cria um DataFrame a partir do resultado
        df = pd.DataFrame(rows)
        # Exibe o DataFrame
        # Salva as alterações no banco de dados
        cnx.commit()
        # Fecha o cursor
        cursor.close()
        if df.iloc[0][0] == 0:
            return 'Account alread exists'
        else:
            return 'Account created'

def ver_carteiras(cnx, username, password):
    with cnx.cursor() as cursor:
        cursor.callproc('verCarteiras', (username, password))
        result = next(cursor.stored_results())
        rows = result.fetchall()
        try:
            df = pd.DataFrame(rows)
            carteiras = df[0].values
            carteiras = np.char.mod('%d', carteiras)
            return carteiras
        except:
            return 'No Wallet'

def ver_categorias_carteira(cnx, username, password, carteira_id, tipo, retorno='padrao'):
    with cnx.cursor() as cursor:
        cursor.callproc('consultarCategorias', (username, password, carteira_id, tipo))
        result = next(cursor.stored_results())
        rows = result.fetchall()
        df = pd.DataFrame(rows)
        if retorno == 'padrao':
            try:
                categorias = df[2].values
                categorias = list(map(str, categorias))
                return categorias
            except:
                return ['Crie uma categoria']
        elif retorno == None:
            categorias = df
            return categorias

def ver_nome_carteira(cnx, username, password, id):
    with cnx.cursor() as cursor:
        cursor.callproc('verCarteiras', (username, password))
        result = next(cursor.stored_results())
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=['id', 'usuario_id', 'nome_carteira', 'descricao', 'saldo'])
        df = df.loc[df['id'] == id]
        try:
            return df.iloc[0][2]
        except:
            return 'Empty'

def ver_saldo_carteira(cnx, username, password, id):
    with cnx.cursor() as cursor:
        cursor.callproc('verSaldo', (username, password, id))
        result = next(cursor.stored_results())
        rows = result.fetchall()
        df = pd.DataFrame(rows)
        try:
            df = df.iloc[0][0]
            return df
        except:
            return 'Empty'

def adicionar_saldo(cnx, username, password, carteira_id, categoria_id, valor):
    with cnx.cursor() as cursor:
        try:
            cursor.callproc('adicionarSaldo', (username, password, carteira_id, categoria_id, valor ))
            cnx.commit()
            return 'Saldo Adicionado'
        except:
            return 'Não foi possivel realizar essa operação'


def retirar_saldo(cnx, username, password, carteira_id, categoria_id, valor):
    with cnx.cursor() as cursor:
        try:
            valor = float(valor)
            cursor.callproc('retirarSaldo', (username, password, carteira_id, categoria_id, valor ))
            result = next(cursor.stored_results())
            rows = result.fetchall()
            df = pd.DataFrame(rows)
            df = df.iloc[0][0]
            return 'Saldo Insuficiente'
        except:
            cnx.rollback()
            try:
                valor = float(valor)
            except:
                return 'Valor Incorreto'
            cursor.callproc('retirarSaldo', (username, password, carteira_id, categoria_id, valor ))
            cnx.commit()
            return 'Saldo Retirado'

def transferir(cnx, username, password, carteira_origem, carteira_destino, valor):
    with cnx.cursor() as cursor:
        try:
            valor = float(valor)
            cursor.callproc('transferirSaldo', (username, password, carteira_origem, carteira_destino, valor))
            result = next(cursor.stored_results())
            rows = result.fetchall()
            df = pd.DataFrame(rows)
            df = df.iloc[0][0]
            return 'Alguma das informações está correta, ou saldo insuficiente'
        except:
            cnx.rollback()
            try:
                valor = float(valor)
            except:
                return 'Valor Incorreto'
            cursor.callproc('transferirSaldo', (username, password, carteira_origem, carteira_destino, valor))
            cnx.commit()
            return 'Saldo transferido'

def criar_categoria(cnx, username, password, cateira_id, tipo, nome, descricao):
    with cnx.cursor() as cursor:
        if tipo == 'e':
            try:
                cursor.callproc('criarCategoriaEntrada', (username, password, cateira_id, nome, descricao))
                result = next(cursor.stored_results())
                result.fetchall()
                return 'Error: criar_categoria()'
            except:
                cnx.rollback()
                cursor.callproc('criarCategoriaEntrada', (username, password, cateira_id, nome, descricao))
                cnx.commit()
                return 'Categoria Created'

        if tipo == 's':
            try:
                cursor.callproc('criarCategoriaSaida', (username, password, cateira_id, nome, descricao))
                result = next(cursor.stored_results())
                result.fetchall()
                return 'Error: criar_categoria()'
            except:
                cnx.rollback()
                cursor.callproc('criarCategoriaSaida', (username, password, cateira_id, nome, descricao))
                cnx.commit()
                return 'Categoria Created'

def deletar_categoria(cnx, username, password, carteira_id, categoria_id, tipo):
    if tipo == 'e':
        with cnx.cursor() as cursor:
            try:
                cursor.callproc('dropCategoria', (username, password, carteira_id, categoria_id, tipo))
                result = next(cursor.stored_results())
                rows = result.fetchall()
                df = pd.DataFrame(rows).iloc[0][0]
                cnx.commit()
                return f'{df}'
            except:
                return 'Erro; deletar_categoria()'
    elif tipo == 's':
        with cnx.cursor() as cursor:
            try:
                cursor.callproc('dropCategoria', (username, password, carteira_id, categoria_id, tipo))
                result = next(cursor.stored_results())
                rows = result.fetchall()
                df = pd.DataFrame(rows).iloc[0][0]
                cnx.commit()
                return f'{df}'
            except:
                return 'Erro; deletar_categoria()'
    else:
        return 'Erro: parametro "Tipo" não é reconhecido.'

def criar_carteira(cnx, username, password, nome):
    with cnx.cursor() as cursor:
        try:
            cursor.callproc('criarCarteira', (username, password, nome, 'None'))
            cnx.commit()
            return 'Carteira Criada'
        except:
            return 'Erro: Criar_carteira()'