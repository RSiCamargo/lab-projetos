# pip install mysql-connector-python
# pip install yagmail
# pip install pixqrcode
# pip install pillow
# pip install openpyxl
# pip install flask-bootstrap
# pip install sqlitedict

from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from datetime import date
import os

# Scripts
import pandas as pd
import scripts.client as cl
import scripts.billing as bill
import scripts.cache as ch
import scripts.stock as st

username = "Usuario Teste"
# Chaves Cache: User_key, Client_"client cpf", Product_"product name", Mail_"client cpf"

name = ''
email = ''
tel = ''
city = ''
type = ''
message = ''
alert = 'none'


class User:
    def __init__(self, name, email, tel, city):
        self.name = name
        self.email = email
        self.tel = tel
        self.city = city


class Client:
    def __init__(self, name, surname, cpf, email, fone, date, discount, status, expense=[], title="", body=""):
        self.name = name
        self.surname = surname
        self.cpf = cpf
        self.email = email
        self.fone = fone
        self.date = date
        self.discount = discount
        self.status = status
        self.expense = expense
        self.title = title
        self.body = body


class Product:
    def __init__(self, product, qnt, cost, price, alert):
        self.product = product
        self.qnt = qnt
        self.cost = cost
        self.price = price
        self.alert = alert


#! --------------------------------------------------------------------------------------------------------------------------------
# ? Dados do Usuário
def configUser(name, email, tel, city):
    oldUser = ch.load("User_key")
    if (name == ""):
        name = oldUser.name

    if (email == ""):
        email = oldUser.email

    if (tel == ""):
        tel = oldUser.tel

    if (city == ""):
        city = oldUser.city

    newUser = User(name, email, tel, city)

    ch.save("User_key", newUser)
    return 0


# ? Cadastrar Cliente
def configClient(name, surname, cpf, email, tel, date, discount, status):
    key = "Client_" + cpf.replace('.', '').replace('-', '')

    client = Client(name, surname, cpf, email, tel, date, discount, status)

    exist = cl.checkClient(key)
    if (not exist):
        ch.save(key, client)
    return 0


# ? Registrar Consumo
def addExpense(cpf, product, qnt):
    pKey = "Product_" + product.lower()

    exist = st.checkProduct(pKey)
    if (exist):
        stockProduct = ch.load(pKey)
    else:
        return 1

    if (int(stockProduct.qnt) < int(qnt)):
        return 2

    key = "Client_" + cpf.replace('.', '').replace('-', '')
    client = ch.load(key)

    newExpenses = {
        "product": stockProduct.product,
        "qnt": qnt,
        "date": str(date.today()),
        "total": float(100 - float(client.discount)) * 0.01 * (float(stockProduct.price) * float(qnt))
    }

    stockProduct.qnt = int(stockProduct.qnt) - int(qnt)
    ch.save(pKey, stockProduct)

    client.expense.append(newExpenses)
    print(client.expense)
    ch.save(key, client)
    alert = 'none'
    return 0


# ? Estoque
def configProduct(product, qnt, cost, price, alert):
    key = "Product_" + product.lower()

    product = Product(product.lower(), qnt, cost, price, alert)

    exist = st.checkProduct(key)
    if (not exist):
        ch.save(key, product)
    else:
        #! add soma de estoque em produto existente
        return False


# ? Estoque
def emailTemplate(cpf, title, body):
    key = "Client_" + cpf.replace('.', '').replace('-', '')
    client = ch.load(key)

    client.title = title
    client.body = body

    ch.save(key, client)


#! --------------------------------------------------------------------------------------------------------------------------------
# ---------------  Running Flask ---------------
app = Flask(__name__)
# app._static_folder = '../content'
app.config['UPLOAD_FOLDER'] = "static/img/"


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        currentDay = 1
        bill.createBilling(currentDay)

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'title.png')
    return render_template('home.html', image=full_filename)


@app.route('/user', methods=['POST', 'GET'])
def user():
    alert = 'none'
    message = 'none'
    type = 'success'

    if request.method == 'POST':
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        tel = request.form.get("tel", "")
        city = request.form.get("city", "")

        if (configUser(name, email, tel, city) == 0):
            alert = 'block'
            message = 'Informações cadastradas!'
            type = 'success'
        else:
            alert = 'block'
            message = 'Usuário já cadastrado!'
            type = 'danger'

    user = ch.load("User_key")

    name = user.name
    email = user.email
    tel = user.tel
    city = user.city
    print(name)

    return render_template('user.html', name=name, email=email, tel=tel, city=city, alert=alert, message=message, type=type)


@app.route('/client', methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        name = request.form.get("name", "")
        surname = request.form.get("surname", "")
        cpf = request.form.get("cpf", "")
        email = request.form.get("email", "")
        tel = request.form.get("tel", "")
        date = request.form.get("date", "")
        discount = request.form.get("discount", "")
        status = request.form.get("status", "")

        configClient(name, surname, cpf, email, tel, date, discount, status)

    return render_template('client.html')


@app.route('/listClients', methods=['POST', 'GET'])
def listClient():
    if request.method == 'POST':
        cl.delClient(request.form.get("delete"))

    clients = cl.clientList()

    return render_template('listClients.html', clients=clients)


@app.route('/expense', methods=['POST', 'GET'])
def expense():
    alert = 'none'
    message = 'none'
    type = 'success'

    if request.method == 'POST':
        cpf = request.form.get("name", "")
        product = request.form.get("product", "")
        qnt = request.form.get("qnt", "")

        res = addExpense(cpf, product, qnt)
        if (res == 1):
            alert = 'block'
            message = 'Produto não existe!'
            type = 'danger'
        elif (res == 2):
            alert = 'block'
            message = 'Quantidade superior ao estoque!'
            type = 'danger'
        else:
            alert = 'block'
            message = 'Consumo cadastrado!'
            type = 'success'

    clients = cl.clientList()

    return render_template('expense.html', clients=clients, alert=alert, message=message, type=type)


@app.route('/stock', methods=['POST', 'GET'])
def stock():
    alert = 'none'
    message = 'none'
    type = 'success'

    if request.method == 'POST':
        product = request.form.get("product", "")
        qnt = request.form.get("qnt", "")
        cost = request.form.get("cost", "")
        price = request.form.get("price", "")
        alert = request.form.get("alert", "")

        if (configProduct(product, qnt, cost, price, alert) == 0):
            alert = 'block'
            message = 'Produto cadastrado no estoque'
            type = 'success'

    return render_template('stock.html', alert=alert, message=message, type=type)


@app.route('/listStock', methods=['POST', 'GET'])
def listStock():
    if request.method == 'POST':
        st.delProduct(request.form.get("delete"))

    products = st.productList()

    return render_template('listStock.html', products=products)


@app.route('/email', methods=['POST', 'GET'])
def emails():
    if request.method == 'POST':
        cpf = request.form.get("name", "")
        title = request.form.get("title", "")
        body = request.form.get("body", "")

        emailTemplate(cpf, title, body)

    clients = cl.clientList()

    return render_template('email.html', clients=clients)


@app.route('/clientExpense', methods=['POST', 'GET'])
def clientExpense():
    expenses = {}

    if request.method == 'POST':
        clientCpf = cpf = request.form.get("name", "")
        key = "Client_" + str(clientCpf).replace('.', '').replace('-', '')
        client = ch.load(key)

        if (bool(client.expense)):
            expenses = client.expense
            # for d in client.expense:
            #     if not list(d.keys())[0] in expenses:
            #         expenses[list(d.keys())[0]] = list(d.values())[0]
            #     else:
            #         val = int(expenses.get(str(list(d.keys())[0])))
            #         expenses[list(d.keys())[0]] = str(
            #             int(list(d.values())[0]) + val)

    clients = cl.clientList()

    return render_template('clientExpense.html', clients=clients, expenses=expenses)


if __name__ == "__main__":
    app.run()
