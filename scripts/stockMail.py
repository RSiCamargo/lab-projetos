import scripts.qrcode as qr
import scripts.cache as ch
import yagmail

# labprojetostestes@gmail.com
# senhalabprojetos


class Billings:
    def __init__(self, name, cpf, email, products=[], title="", body="", day=""):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.products = products


def createBilling(currentDay):
    clients = ch.loadAll("Client")
    user = ch.load("User_key")

    userEmail = 'labprojetostestes@gmail.com'
    app_password = 'qtlprqhrqwgtzpch'  # Token for gmail

    for client in clients:
        total = 0
        if (int(client.date) == int(currentDay)):
            print(client.date)
            productList = []
            amountList = []
            totalList = []

            for expense in client.expense:
                total += float(expense["total"])

                productList.append(expense["product"])
                amountList.append(expense["qnt"])
                totalList.append(expense["total"])

            list = ""
            lista = []

            for num in range(len(productList)):
                list = f'<span style="border-bottom: 1px solid lightgray;display: inline-block;width: 100%;padding-left:40px"><p style="text-align: left;display: inline-block;width: 70%;">{productList[num]}</p><i>{amountList[num]}</i><a style="text-align: right;display: inline-block;width: 15%;position: relative;">R${totalList[num]}</a></span>'
                lista.append(list)

            qr.generateQRCode(user, client.name, str(total * 10))
            qri = f"./static/generatedpix/pix-{client.name}.png"

            if (client.title == ""):
                title = f'Cobrança à {client.name}'
            else:
                title = client.title

            if (client.body == ""):
                body = f'Este é um email referente à cobrança gerada por {user.name}.'
            else:
                body = client.body

            items = ["&emsp;{}".format(s) for s in lista]
            items = "".join(items)
            subject = f'{title}'
            content = ['<div style="text-align: center;background-color: #e1e1e1;"><div>',
                       f'<h2>Olá {client.name},</h2><p style="font-size: large">{body}</p><p style="font-size: large">Em anexo segue o código pix referente ao valor de R${total}.</p></div>',
                       f'<div style="border: solid 1px gray; width: 1000px; margin: 0 auto; background-color: white; box-shadow: 2px 2px #86868621"><header>',
                       yagmail.inline("./static/img/title.png"),
                       f'</header><section><article><h1 style="text-align: center">Resumo da compra</h1><div style="width: 100%;"><a style="width: 65%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Produto</a><a style="width: 12.5%; padding-left: 2.5%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Quantidade</a><a style="width: 9%; padding-left: 1%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Valor</a></div>',
                       items,
                       f'<div style="border-top: 2px solid black"><p style="width: 95%;text-align: right;font-family: sans-serif;font-size: large;font-weight: bold;">Total: R${total}</p></div></article></section></div>',
                       yagmail.inline(
                           f"./static/generatedpix/pix-{client.name}.png"),
                       '<footer style="margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;text-align: center"><p style="padding: 0px;margin: 5px;">Ward - Automated Billing Service</p><p style="padding: 0px;margin: 5px;">Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p style="padding: 0px;margin: 5px;">Nos contate em labprojetospuc@gmail.com</p></footer></div>']
            attachments = [qri]

            with yagmail.SMTP(userEmail, app_password) as yag:
                yag.send(client.email, subject, content, attachments)
                print('Sent email successfully')
