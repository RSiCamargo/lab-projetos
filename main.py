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
import datetime
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
    user = User(name, email, tel, city)
    ch.save("User_key", user)


# ? Cadastrar Cliente
def configClient(name, surname, cpf, email, tel, date, discount, status):
    key = "Client_" + cpf.replace('.', '').replace('-', '')

    client = Client(name, surname, cpf, email, tel, date, discount, status)

    exist = cl.checkClient(key)
    if (not exist):
        ch.save(key, client)


# ? Registrar Consumo
def addExpense(cpf, product, qnt):
    pKey = "Product_" + product.lower()

    exist = st.checkProduct(pKey)
    if (exist):
        stockProduct = ch.load(pKey)
    else:
        #! Add alerta
        return

    if (int(stockProduct.qnt) < int(qnt)):
        #! Add alerta
        return

    key = "Client_" + cpf.replace('.', '').replace('-', '')
    client = ch.load(key)

    newExpenses = {
        stockProduct.product: qnt
    }

    stockProduct.qnt = int(stockProduct.qnt) - int(qnt)
    ch.save(pKey, stockProduct)

    client.expense.append(newExpenses)
    ch.save(key, client)


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


#!
# ? Forçar Faturamento
    currentDay = 5
    bill.createBilling(currentDay)

# ? Agenda (Por último, caso dê tempo)


#! --------------------------------------------------------------------------------------------------------------------------------
# ---------------  Running Flask ---------------
app = Flask(__name__)
# app._static_folder = '../content'
app.config['UPLOAD_FOLDER'] = "static/img/"


@app.route("/")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'title.png')
    return render_template('home.html', image=full_filename)


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
    if request.method == 'POST':
        cpf = request.form.get("name", "")
        product = request.form.get("product", "")
        qnt = request.form.get("qnt", "")

        addExpense(cpf, product, qnt)

    clients = cl.clientList()

    return render_template('expense.html', clients=clients)


@app.route('/stock', methods=['POST', 'GET'])
def stock():
    if request.method == 'POST':
        product = request.form.get("product", "")
        qnt = request.form.get("qnt", "")
        cost = request.form.get("cost", "")
        price = request.form.get("price", "")
        alert = request.form.get("alert", "")

        configProduct(product, qnt, cost, price, alert)

    return render_template('stock.html')


@app.route('/listStock', methods=['POST', 'GET'])
def listStock():
    if request.method == 'POST':
        st.delProduct(request.form.get("delete"))

    products = st.productList()

    return render_template('listStock.html', products=products)


@app.route('/email', methods=['POST', 'GET'])
def email():
    return render_template('email.html')


if __name__ == "__main__":
    app.run()
