import scripts.emails as mail
import scripts.qrcode as qr
import scripts.cache as ch
import scripts.stock as st


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

class Product:
    def __init__(self, name, amount, unitPrice):
        self.name = name
        self.amount = amount
        self.unitPrice = unitPrice


def createBilling(currentDay):
    billings = ch.loadAll("Billings_")
    products = []
    stock = st.importStock()

    user = ch.load("User_key")

    for day in billings.day:
        total = 0
        if (day == currentDay):
            key = "Client_" + billings.cpf.replace('.', '-')
            client = ch.load(key)

            for a, b in client.expense:
                for name, price in stock:
                    if name == a:
                        c = price

                total = total + b * c
                products.append(Product(a, b, c))

            pix = qr.generateQRCode(user, client.name, str(total))
            qr = f"./static/generatedpix/pix-{client.name}.png"

            mail.sendBillingMail(qr, billings, products, total)
