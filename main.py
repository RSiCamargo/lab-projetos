# pip install mysql-connector-python
# pip install yagmail
# pip install pixqrcode
# pip install pillow
# pip install openpyxl
# pip install flask-bootstrap
# pip install sqlitedict

from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import datetime
import os

# Scripts
import scripts.client as cl
import scripts.billing as bill
import scripts.cache as ch
import scripts.stock as st

username = "Usuario Teste"
# Chaves Cache: User_key, Client_"client cpf", Product_"product name", Billing_"client cpf"

name = ''
email = ''
tel = ''
city = ''


class User:
    def __init__(self, name, email, tel, city):
        self.name = name
        self.email = email
        self.tel = tel
        self.city = city


class Client:
    def __init__(self, name, surname, cpf, email, fone, date, status, expense):
        self.name = name
        self.surname = surname
        self.cpf = cpf
        self.email = email
        self.fone = fone
        self.date = date
        self.status = status
        self.expense = expense


class Billings:
    def __init__(self, name, cpf, email, title, body, day):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.title = title
        self.body = body
        self.day = day


#! --------------------------------------------------------------------------------------------------------------------------------
# ? Dados do Usuário
def configUser(name, email, tel, city):
    user = User(name, email, tel, city)
    ch.save("User_key", user)


# ? Cadastrar Cliente
def configClient(name, surname, cpf, email, tel, date, status):
    key = "Client_" + cpf.replace('.', '-')

    client = Client(name, surname, cpf, email, tel, date, status)

    response = cl.checkClient(key)
    if (response):
        ch.save(key, client)


# ? Registrar Consumo
def loadClientExpense():
    # Da pra alterar a funcao pra escolher o cliente direto na caixa de texto (Esperar Front)

    # Pegar do front:
    clientName = ""
    clientCpf = ""

    # Add busca por cpf
    results = cl.findByName(clientName)
    if len(results) == 0:
        # alerta cliente não existe
        print(True)
    elif len(results) > 1:
        # alerta pedindo pra preencher o cpf do desejado (listar os cpfs)
        for client in results:
            print(client.cpf)
    else:
        # Adicionar no front o nome e cpf do cliente desejado
        print(True)


def addExpense():
    # Pegar do front:
    clientCpf = ""

    key = "Client_" + clientCpf.replace('.', '-')

    results = ch.load(key)
    client = Client(results.name, results.surname, results.cpf,
                    results.email, results.tel, results.date, results.status, results.expense)

    newExpenses = {}  # Pegar do front o dict produto/valor, e adicionar.
    client.expense.append(newExpenses)
    ch.save(key, client)


# ? Estoque
# Ver como estara o front para fazer as interações
# st.addProduct()
# st.removeProduct()
# st.editProduct()
# st.checkStock()


# ? Editar Faturamento
def loadClientBilling():
    # Da pra alterar a funcao pra escolher o cliente direto na caixa de texto (Esperar Front)

    # Pegar do front:
    clientName = ""
    clientCpf = ""

    # Add busca por cpf
    results = cl.findByName(clientName)
    if len(results) == 0:
        # alerta cliente não existe
        print(True)
    elif len(results) > 1:
        # alerta pedindo pra preencher o cpf do desejado (listar os cpfs)
        for client in results:
            print(client.cpf)
    else:
        # Adicionar no front o nome, cpf e email do cliente desejado
        print(True)

    # Arrumar
    client = Client(results.name, results.surname, results.cpf,
                    results.email, results.tel, results.date, results.status, results.expense)


def scheduleBilling():
    # Pegar do front:
    clientName = ""
    clientCpf = ""
    billingDay = ""
    email = ""
    emailTitle = ""
    emailBody = ""

    newBilling = Billings(clientName, clientCpf, email,
                          emailTitle, emailBody, billingDay)

    key = "Billing_" + clientCpf.replace('.', '-')
    ch.save(key, newBilling)


# ? Scheduler
    # Rodar diariamente
    currentDay = ""
    bill.createBilling(currentDay)

# ? Agenda (Por último, caso dê tempo)


#! --------------------------------------------------------------------------------------------------------------------------------
# ---------------  Running Flask ---------------
# Futuro: Pegar novo do usuario pela sessao/cadastro/etc... e adicionar ou novo do arquivo de upload
app = Flask(__name__)
app._static_folder = '../content'
#app.config['UPLOAD_FOLDER'] = "static/uploadedexcel/"


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        tel = request.form.get("tel", "")
        city = request.form.get("city", "")

        configUser(name, email, tel, city)

    user = ch.load("User_key")

    name = user.name
    email = user.email
    tel = user.tel
    city = user.city

    return render_template('user.html', name=name, email=email, tel=tel, city=city)


@app.route('/client', methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        name = request.form.get("name", "")
        surname = request.form.get("surname", "")
        cpf = request.form.get("cpf", "")
        email = request.form.get("email", "")
        tel = request.form.get("tel", "")
        date = request.form.get("date", "")
        status = request.form.get("status", "")

        configClient(name, surname, cpf, email, tel, date, status)

    return render_template('client.html')


@app.route('/listClients', methods=['POST', 'GET'])
def listClient():
    clients = cl.clientList()
    clientsTable = ''

    for cl in clients:
        clientsTable = clientsTable + \
            f"<tr><td>{clients.index(cl) + 1}</td><td>{cl.name}</td><td>{cl.date}</td><td>{cl.status}</td></tr>"

    return render_template('listClients.html', clientsTable=clientsTable)


@app.route('/expense', methods=['POST', 'GET'])
def expense():
    return render_template('expense.html')


@app.route('/stock', methods=['POST', 'GET'])
def stock():
    return render_template('stock.html')


@app.route('/listStock', methods=['POST', 'GET'])
def listStock():
    return render_template('listStock.html')


@app.route('/email', methods=['POST', 'GET'])
def email():
    return render_template('email.html')


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
if __name__ == "__main__":
    app.run()
