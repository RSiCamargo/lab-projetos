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
# Chaves Cache: User_key, Client_"client cpf", Product_"product name"


class User:
    def __init__(self, name, email, tel, city):
        self.name = name
        self.email = email
        self.tel = tel
        self.city = city


class Client:
    def __init__(self, name, surname, cpf, email, fone, date, status, expense=[]):
        self.name = name
        self.surname = surname
        self.cpf = cpf
        self.email = email
        self.fone = fone
        self.date = date
        self.status = status
        self.expense = []


class Product:
    def __init__(self, name, amount, unitPrice):
        self.name = name
        self.amount = amount
        self.unitPrice = unitPrice

#! --------------------------------------------------------------------------------------------------------------------------------


# ? Dados do Usuário
def configUser():
    # Pegar do front:
    name = ""
    email = ""
    tel = ""
    city = ""

    user = User(name, email, tel, city)
    ch.save("User_key", user)


# ? Cadastrar Cliente
def configClient():
    # Pegar do front:
    name = ""
    surname = ""
    cpf = ""
    email = ""
    tel = ""
    date = ""
    status = True

    key = "Client_" + cpf.replace('.', '-')

    client = Client(name, surname, cpf, email, tel, date, status)

    response = cl.checkClient(key)
    if (response):
        ch.save(key, client)


# ? Listagem de Clientes
def listAllClients():
    clients = cl.clientList()

    # Criar elemento html (Esperar front para sincronizar formatação da tabela)


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
                    results.email, results.tel, results.date, results.status)

    newExpenses = []  # Pegar do front as tuplas produto/valor, e adicionar.
    client.expense.append(newExpenses)
    ch.save


# ? Estoque
# Ver como estara o front para fazer as interações
st.addProduct()
st.removeProduct()
st.editProduct()
st.checkStock()


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
        # Adicionar no front o nome e cpf do cliente desejado
        print(True)


# Pegar do front:
emailTitle = ""
emailBody = ""
emailEnd = ""

bill.createBilling(emailTitle, emailBody, emailEnd)


# ? Agenda (Por último, caso dê tempo)

#! --------------------------------------------------------------------------------------------------------------------------------
# ---------------  Running Flask ---------------
# Futuro: Pegar novo do usuario pela sessao/cadastro/etc... e adicionar ou novo do arquivo de upload
app = Flask(__name__)
app._static_folder = '../content'
app.config['UPLOAD_FOLDER'] = "static/uploadedexcel/"


@app.route("/")
def home():
    return render_template('index.html', username=username)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(app.config['UPLOAD_FOLDER'] + f.filename)

        try:
            fn = "static/uploadedexcel/" + os.path.basename(f.filename)
            input_sheet = load_workbook(fn)
            sheet = input_sheet.active
        except ValueError:
            print("Erro no upload de arquivo. Será aceita apenas a extensão .xlsx")

        code = sheet["AA1"].value
        if code == 'expense':
            readExpenseFile(sheet)
            return "Upload do arquivo de consumo efetuado com sucesso!"
        elif code == 'stock':
            readStockFile(sheet)
            return "Upload do arquivo de estoque efetuado com sucesso!"
        elif code == 'dados':
            readDataFile(sheet)
            return "Upload do arquivo de dados efetuado com sucesso!"
        else:
            return 'O arquivo não pode ser validado. Por favor utilize os templates disponíveis no github!'


@app.route('/daily', methods=['POST', 'GET'])
def daily():
    if request.method == 'POST':
        if request.form['help'] == 'Call Routines':
            try:
                createBilling()
            except ValueError:
                return "Erro ao gerar faturamento!"
            try:
                checkStock()
            except ValueError:
                return "Erro ao realizar a verificação do estoque!"

            return "Faturamento e checagem de estoque rodados com sucesso!!"
        elif request.form['help'] == 'Clean DB':
            cleanDatabase()
            return "Dados de teste excluidos do DB"


if __name__ == "__main__":
    app.run()
