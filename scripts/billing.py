import scripts.qrcode as qr
import scripts.cache as ch
import scripts.stock as st
import yagmail


# def createBilling():
#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
#     cursor = connection.cursor()

#     # Vai checar quais os clientes finais possuem faturamentos no dia
#     print("Gerando Faturamento")
#     stmt = ("SELECT CURDATE()")
#     cursor.execute(stmt)

#     for row in cursor:
#         date = row[0]

#     day = date.strftime("%d")
#     stmt = ("SELECT userPix,cons.clientName,email,city,userName,GROUP_CONCAT(price),GROUP_CONCAT(product),GROUP_CONCAT(amount) FROM data,cons WHERE billingDay = %s and data.clientName = cons.clientName group by userPix")
#     d = (day,)
#     cursor.execute(stmt, d)
#     row = cursor.fetchall()

#     for all in row:
#         # print(all[0], all[1], all[2], all[3], all[4], all[5], all[6], all[7])
#         priceList = all[5].split(',')
#         total = sum(float(i) for i in priceList)
#         total = int(total * 100)

#         currentUser = User(all[4], "null", all[0])
#         currentClient = Client(all[1], all[2], all[3], "null")
#         currentProduct = Product(all[6].split(
#             ','), all[7].split(','), priceList)

#         pix = qr.generateQRCode(
#             all[0], all[3], all[4], str(total), all[1])

#         qr = f"./static/generatedpix/pix-{all[1]}.png"

#         mail.sendBillingMail(
#             qr, currentClient, currentUser, currentProduct, total)

#     print("Fechando Faturamento")

class Billings:
    def __init__(self, name, cpf, email, products=[], title="", body="", day=""):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.products = products


def createBilling(currentDay):
    clients = ch.loadAll("Clients")
    user = ch.load("User_key")

    userEmail = 'labprojetospuc@gmail.com'
    app_password = 'npfyvwfaljvlvplv'  # Token for gmail
    #to = billing.email

    for day in clients.date:
        total = 0
        if (day == currentDay):
            for a, b in clients.expense:
                pKey = "Product_" + a
                product = ch.load(pKey)

                total += int(b) * product.price

                productList = products.name
                amountList = products.amount
                priceList = products.unitPrice

                list = ""
                lista = []

                for num in range(len(productList)):
                    list = f'<span style="border-bottom: 1px solid lightgray;display: inline-block;width: 100%;padding-left:40px"><p style="text-align: left;display: inline-block;width: 70%;">{productList[num]}</p><i>{amountList[num]}</i><a style="text-align: right;display: inline-block;width: 15%;position: relative;">R${priceList[num]}</a></span>'
                    lista.append(list)

                items = ["&emsp;{}".format(s) for s in lista]
                items = "".join(items)
                subject = f'{billing.title}'
                content = ['<div style="text-align: center;background-color: #e1e1e1;"><div>',
                           f'<p style="font-size: large,text-align: center">{billing.body}</p></div>',
                           f'<header>',
                           yagmail.inline("./static/img/title.png"),
                           f'</header><section><article><h1 style="text-align: center">Resumo da compra</h1><div style="width: 100%;"><a style="width: 65%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Produto</a><a style="width: 12.5%; padding-left: 2.5%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Quantidade</a><a style="width: 9%; padding-left: 1%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Preço</a></div>',
                           items,
                           f'<div style="border-top: 2px solid black"><p style="width: 95%;text-align: right;font-family: sans-serif;font-size: large;font-weight: bold;">Total: R${total}</p></div></article></section></div>',
                           yagmail.inline(
                               f"./static/generatedpix/pix-{billing.name}.png"),
                           '<footer style="margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;text-align: center"><p style="padding: 0px;margin: 5px;">Ward - Automated Billing Service</p><p style="padding: 0px;margin: 5px;">Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p style="padding: 0px;margin: 5px;">Nos contate em labprojetospuc@gmail.com</p></footer></div>']
                attachments = [qr]

                with yagmail.SMTP(userEmail, app_password) as yag:
                    yag.send(to, subject, content, attachments)
                    print('Sent email successfully')

                total = total + b * c
                products.append(Product(a, b, c))

            pix = qr.generateQRCode(user, client.name, str(total))
            qr = f"./static/generatedpix/pix-{client.name}.png"

            mail.sendBillingMail(qr, billings, products, total)
