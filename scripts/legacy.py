# from mysql.connector import Error
# import mysql.connector
# from openpyxl import load_workbook

# region Banco
# --------------- Cria a conexão com o banco de dados ---------------
# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print("Connection to MySQL DB successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")

#     return connection


# # --------------- Função para execução de single queries ---------------
# def execute_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         connection.commit()
#         return True
#     except Error as e:
#         return False


# def cleanDatabase():
#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
#     cursor = connection.cursor()
#     stmt = ("DELETE FROM cons WHERE clientName='Cliente Apresentacao'")
#     cursor.execute(stmt)
#     connection.commit()
#     stmt = ("DELETE FROM data WHERE clientName='Cliente Apresentacao';")
#     cursor.execute(stmt)
#     connection.commit()
#     stmt = ("DELETE FROM stock WHERE product = 'Produto 1';")
#     cursor.execute(stmt)
#     connection.commit()
#     stmt = ("DELETE FROM stock WHERE product = 'Produto 2';")
#     cursor.execute(stmt)
#     connection.commit()
#     print("Remoções realizadas no banco")

# endregion

# region Consumo de Arquivos
# --------------- Arquivos de Dados ---------------
# def readDataFile(file):
#     userEmail = file["D3"].value
#     userPix = file["D5"].value

#     for value in file.iter_rows(min_row=8, min_col=3, max_col=7, values_only=True):
#         if (value[0] != None):
#             updateUser(value[0], value[2], value[3],
#                        value[4], username, userPix, userEmail)
#         else:
#             break


# --------------- Arquivo de Consumo ---------------
# def readExpenseFile(file):
#     date = file["D1"].value

#     for value in file.iter_rows(min_row=4, min_col=3, max_col=6, values_only=True):
#         if (value[0] != None):
#             checkClientAndSave(value[0], value[1], value[2], value[3], date)
#         else:
#             break


# # --------------- Arquivo de Estoque ---------------
# def readStockFile(file):
#     for value in file.iter_rows(min_row=4, min_col=3, max_col=6, values_only=True):
#         if (value[0] != None):
#             updateStockAndSave(value[0], value[1], id, value[3], value[2])
#         else:
#             break

# endregion

# region Metodos
# def updateUser(clientName, billingDay, email, city, userName, userPix, userEmail):
#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")

#     print(f"O User {userName} com o Pix {userPix}, adicionou o cliente {clientName}, residente da cidade {city} e com email {email}, com faturamento agendado para o dia {billingDay}")

#     cursor = connection.cursor()
#     stmt = ("INSERT INTO data (clientName, billingDay, email, city, userName ,userPix, userEmail) VALUES (%s, %s, %s, %s, %s, %s, %s)")
#     values = (clientName, billingDay, email,
#               city, userName, userPix, userEmail)
#     cursor.execute(stmt, values)
#     connection.commit()
#     cursor.close


# def checkClientAndSave(nome, insumo, quantidade, preco, created_at):

#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
#     cursor = connection.cursor()

#     # Checar se o cliente existe, e salvar no banco (alertar se o cliente não existir)
#     query = ("SELECT CASE WHEN EXISTS (SELECT  clientName FROM data  WHERE clientName = %s) THEN 1 ELSE 0 END ")
#     name = (nome,)
#     cursor.execute(query, name)
#     for row in cursor:
#         checkName = row[0]

#     if (checkName == 1):
#         print("Existe no banco")
#         print(
#             f"O cliente {nome} comprou {insumo}, quantidade {quantidade} e com porcentagem de  {preco},  criado em {created_at}")
#         stmt = 'INSERT INTO cons (clientName, product, amount, price ,created_at) VALUES (%s, %s, %s, %s, %s)'
#         data = (nome, insumo, quantidade, preco, created_at)
#         cursor.execute(stmt, data)
#         connection.commit()

#         stmt = (
#             "SELECT id,amount,product FROM cons WHERE id=(SELECT LAST_INSERT_ID()) ")
#         cursor.execute(stmt)
#         for row in cursor:
#             id = row[0]
#             quantidade = row[1]
#             insumo = row[2]

#         updateStockAndSave(insumo, quantidade, id, "proxUpdate")
#         cursor.close
#     else:
#         print("Cliente não cadastrado no banco")


# def updateStockAndSave(insumo, quantidade, id, alerta, preco=0):
#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
#     cursor = connection.cursor()
#     if (preco != 0):
#         # Entrará aqui se o arquivo for para atualizacao de estoque.
#         stmt = (
#             "INSERT INTO stock (product, amount, price, warning) VALUES (%s, %s , %s, %s)")
#         values = (insumo, quantidade, preco, alerta)
#         cursor.execute(stmt, values)
#         connection.commit()
#         cursor.close
#         print(
#             f"Foi adicionado {quantidade} unidades do insumo {insumo} ajustado ao custo base de {preco} - alerta de baixo estoque settado em {alerta} unidades")
#     else:
#         # Entrará aqui se o arquivo for para a retirada de estoque.
#         stmt = ("UPDATE stock SET amount = amount - %s WHERE product = %s")
#         data = (quantidade, insumo)
#         cursor.execute(stmt, data)
#         connection.commit()
#         cursor.close
#         print(
#             f"Foi retirado {quantidade} unidades do insumo {insumo} no estoque")
# endregion


# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(app.config['UPLOAD_FOLDER'] + f.filename)

#         try:
#             fn = "static/uploadedexcel/" + os.path.basename(f.filename)
#             input_sheet = load_workbook(fn)
#             sheet = input_sheet.active
#         except ValueError:
#             print("Erro no upload de arquivo. Será aceita apenas a extensão .xlsx")

#         code = sheet["AA1"].value
#         if code == 'expense':
#             readExpenseFile(sheet)
#             return "Upload do arquivo de consumo efetuado com sucesso!"
#         elif code == 'stock':
#             readStockFile(sheet)
#             return "Upload do arquivo de estoque efetuado com sucesso!"
#         elif code == 'dados':
#             readDataFile(sheet)
#             return "Upload do arquivo de dados efetuado com sucesso!"
#         else:
#             return 'O arquivo não pode ser validado. Por favor utilize os templates disponíveis no github!'


# @app.route('/daily', methods=['POST', 'GET'])
# def daily():
#     if request.method == 'POST':
#         if request.form['help'] == 'Call Routines':
#             try:
#                 createBilling()
#             except ValueError:
#                 return "Erro ao gerar faturamento!"
#             try:
#                 checkStock()
#             except ValueError:
#                 return "Erro ao realizar a verificação do estoque!"

#             return "Faturamento e checagem de estoque rodados com sucesso!!"
#         elif request.form['help'] == 'Clean DB':
#             cleanDatabase()
#             return "Dados de teste excluidos do DB"
