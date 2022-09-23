# !pip install mysql-connector-python
# !pip install yagmail
# !pip install pixqrcode
# !pip install flask-ngrok

from flask_ngrok import run_with_ngrok
from flask import Flask, render_template
from pixqrcode import PixQrCode
from openpyxl import load_workbook
from mysql.connector import Error
import yagmail
import mysql.connector
import datetime
import os
import cgi
import os
import cgitb
cgitb.enable()


# --------------- Cria a conexão com o banco de dados ---------------

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# --------------- Função para execução de single queries ---------------


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        return False


# --------------- Arquivo de Dados ---------------
def readDataFile(file):
    username = file["D3"].value
    userEmail = file["D4"].value
    userPix = file["D6"].value

    for value in file.iter_rows(min_row=9, min_col=3, max_col=7, values_only=True):
        if (value[0] != None):
            updateUser(value[0], value[2], value[3],
                       value[4], username, userPix, userEmail)
        else:
            break


def updateUser(clientName, billingDay, email, city, userName, userPix, userEmail):
    connection = create_connection(
        "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
    # Salvar no banco as infos do usuário, e fazer o update da lista de clientes (trabalhar com tudo minusculo)
    print(f"O User {userName} com o Pix {userPix}, adicionou o cliente {clientName}, residente da cidade {city} e com email {email}, com faturamento agendado para o dia {billingDay}")
    cursor = connection.cursor()
    stmt = ("INSERT INTO data (clientName, billingDay, email, city, userName ,userPix, userEmail) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    values = (clientName, billingDay, email,
              city, userName, userPix, userEmail)
    cursor.execute(stmt, values)
    connection.commit()
    cursor.close


# --------------- Arquivo de Consumo ---------------

def readExpenseFile(file):
    date = file["D1"].value

    for value in file.iter_rows(min_row=4, min_col=3, max_col=6, values_only=True):
        if (value[0] != None):
            checkClientAndSave(value[0], value[1], value[2], value[3], date)
        else:
            break


def checkClientAndSave(nome, insumo, quantidade, porcentagem, created_at):

    connection = create_connection(
        "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
    cursor = connection.cursor()

    # Checar se o cliente existe, e salvar no banco (alertar se o cliente não existir)
    query = ("SELECT CASE WHEN EXISTS (SELECT  clientName FROM data  WHERE clientName = %s) THEN 1 ELSE 0 END ")
    name = (nome,)
    cursor.execute(query, name)
    for row in cursor:
        checkName = row[0]

    if (checkName == 1):
        print("Existe no banco")
        print(
            f"O cliente {nome} comprou {insumo}, quantidade {quantidade} e com porcentagem de  {porcentagem},  criado em {created_at}")
        stmt = 'INSERT INTO cons (clientName, product, amount, percentage ,created_at) VALUES (%s, %s, %s, %s, %s)'
        data = (nome, insumo, quantidade, porcentagem, created_at)
        cursor.execute(stmt, data)
        connection.commit()

        stmt = (
            "SELECT id,amount,product FROM cons WHERE id=(SELECT LAST_INSERT_ID()) ")
        cursor.execute(stmt)
        for row in cursor:
            id = row[0]
            quantidade = row[1]
            insumo = row[2]

        updateStockAndSave(insumo, quantidade, id)
        cursor.close
    else:
        print("Cliente não cadastrado no banco")


# --------------- Arquivo de Estoque ---------------
def readStockFile(file):
    for value in file.iter_rows(min_row=4, min_col=3, max_col=6, values_only=True):
        updateStockAndSave(value[0], value[1], id, value[3], value[2])


def updateStockAndSave(insumo, quantidade, id, alerta, preco=0):
    connection = create_connection(
        "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
    cursor = connection.cursor()
    if (preco != 0):
        # Entrará aqui se o arquivo for para atualizacao de estoque.
        stmt = (
            "INSERT INTO stock (product, amount, price, warning) VALUES (%s, %s , %s, %s)")
        values = (insumo, quantidade, preco, alerta)
        cursor.execute(stmt, values)
        connection.commit()
        cursor.close
        print(
            f"Foi adicionado {quantidade} unidades do insumo {insumo} ajustado ao custo base de {preco} - alerta de baixo estoque settado em {alerta} unidades")
    else:
        # Entrará aqui se o arquivo for para a retirada de estoque.
        stmt = ("UPDATE stock SET amount = amount - %s WHERE product = %s")
        data = (quantidade, insumo)
        cursor.execute(stmt, data)
        connection.commit()
        cursor.close
        print(
            f"Foi retirado {quantidade} unidades do insumo {insumo} no estoque")


# --------------- Rotina de Faturamento ---------------
def createBilling():
    connection = create_connection(
        "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
    cursor = connection.cursor()

    # Vai checar quais os clientes finais possuem faturamentos no dia
    print("Gerando Faturamento")
    stmt = ("SELECT CURDATE()")
    cursor.execute(stmt)

    for row in cursor:
        date = row[0]

    day = date.strftime("%d")
    stmt = ("SELECT cons.clientName,product,amount,percentage,email FROM cons,data WHERE billingDay = %s AND cons.clientName = data.clientName")
    d = (day,)
    cursor.execute(stmt, d)
    row = cursor.fetchall()

    for index, all in row:
        # loop dos registros
        print(all[0], all[1], all[2], all[3], all[4])
        if ():
            print('teste')

        # checkout = XXX*(all[4]/100) Buscar valor do produto no estoque do usuario
        # Buscando apenas 1 produto, integrar todos os retornados

        # pix = generateQRCode(all[0], all[2], all[3], all[4])
        # img = f"/content/static/generatedpix/pix-{all[3]}.png"

        # sendBillingMail(img, all[1], all[3], all[4], all[5], all[6])

    print("Fechando Faturamento")

# FALTA ARRUMAR O VALOR PASSADO PARA O PIX QRCODE


def generateQRCode(userPix, city, username, value):
    pix = PixQrCode(username, userPix, city, value)

    if pix.is_valid():
        pix.save_qrcode("/content/static/generatedpix", f"pix-{username}")
        return pix.generate_code()
    else:
        return "Dados para Pix inválidos."


# --------------- Envio de Email ---------------

def sendStockAlertMail(product, amount, userEmail):
    user = 'labprojetospuc@gmail.com'
    app_password = 'npfyvwfaljvlvplv'  # Token for gmail
    to = userEmail

    subject = 'Aviso de estoque'
    content = [
        f'<h3>O(s) produto(s) {product} de seu estoque chegaram a marca de alerta ou foram zerados!</h3>']

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')


def sendBillingMail(qr, client, clientMail, userName, value, product, amount, total):
    user = 'labprojetospuc@gmail.com'
    app_password = 'npfyvwfaljvlvplv'  # Token for gmail
    to = clientMail

    lista = f'<span><p>{product}</p><i>{amount}</i><a>R$10,00</a></span>'

    subject = f'Cobrança à {userName}'
    content = ['<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="X-UA-Compatible" content="ie=edge"><style>body {text-align: center;background-color: #e1e1e1;}section {height: 800px;}footer {margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;}footer p {padding: 0px;margin: 5px;}article span p {text-align: left;display: inline-block;width: 70%;}article span a {text-align: right;display: inline-block;width: 15%;position: relative;}article span {border-bottom: 1px solid lightgray;display: inline-block;width: 100%;}article div {width: 100%;}article div p{width: 95%;text-align: right;font-family: sans-serif;font-size: large;font-weight: bold;}article div a {display: inline-block;position: relative;font-weight: bold;text-align: left;}</style></head><body><div>',
               f'<h2>Olá {client},</h2><p style="font-size: large">Este é um email referente à cobrança gerada por {userName}. Em anexo segue o código pix referente ao valor de R${total}.</p></div>',
               '<div style="border: solid 1px gray; width: 1000px; margin: 0 auto; background-color: white; box-shadow: 2px 2px #86868621"><header><img src="./content/static/img/title.png" alt="header" width="1000" height="100"></header><section><article><h1>Resumo da compra</h1><div><a style="width: 65%; padding-left: 3%">Produto</a><a style="width: 12.5%; padding-left: 2.5%">Quantidade</a><a style="width: 9%; padding-left: 1%">Preço(un.)</a></div>',
               lista,
               '<div style="border-top: 2px solid black"><p>Total: R$30,00</p></div></article></section></div><footer><p>Ward - Automated Billing Service</p><p>Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p>Nos contate em labprojetospuc@gmail.com</p></footer></body></html>']
    attachments = [qr]

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content, attachments)
        print('Sent email successfully')


# --------------- Rotina de Controle de Estoque ---------------
def checkStock():
    # Vai checar, para cada user, como estao os estoques
    connection = create_connection(
        "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
    cursor = connection.cursor()
    stmt = ("SELECT product,amount,userEmail FROM stock,data WHERE amount = 0")
    cursor.execute(stmt)
    row = cursor.fetchall()
    for all in row:
        sendStockAlertMail(all[0], all[1], all[2])

    stmt = ("SELECT product,amount,userEmail FROM stock,data WHERE amount = warning GROUP BY product,amount,userEmail ")
    cursor.execute(stmt)
    row = cursor.fetchall()
    for all in row:
        sendStockAlertMail(all[0], all[1], all[2])
    cursor.close

# --------------- Controle de Rotinas ---------------


def callDailyRoutines():
    try:
        createBilling()
    except ValueError:
        print("Erro ao gerar faturamento!")
    try:
        checkStock()
    except ValueError:
        print("Erro ao realizar a verificação do estoque!")


callDailyRoutines()


app = Flask(__name__)
app._static_folder = '/content'
run_with_ngrok(app)


@app.route("/")
def home():
    return render_template('index.html')


app.run()


form = cgi.FieldStorage()
fileitem = form['filename']

if fileitem.filename:
    fn = os.path.basename(fileitem.filename)

    try:
        # Aqui entrar o arquivo de upload
        input_sheet = load_workbook(filename=fn)
    except ValueError:
        print("Erro no upload de arquivo. Será aceita apenas a extensão .xlsx")

else:
    print("Nenhum arquivo foi anexado")


sheet = input_sheet.active  # Selecionar a planilha pra trabalhar
code = sheet["AA1"].value

if code == 'expense':
    readExpenseFile(sheet)
elif code == 'stock':
    readStockFile(sheet)
elif code == 'dados':
    readDataFile(sheet)
else:
    print('O arquivo não pode ser validado. Por favor utilize os templates disponíveis no github!')