# add product
# remove product
# edit product quantity
# edit product price
# check stock after something is used (alert if below limit)


# Alterar pra mostrar um banner ou algo do tipo
# def checkStock():
#     # Vai checar, para cada user, como estao os estoques
#     connection = create_connection(
#         "us-cdbr-east-06.cleardb.net", "b090112be85288", "2f84fdce", "heroku_7324e25c80c3d90")
#     cursor = connection.cursor()
#     stmt = ("SELECT GROUP_CONCAT(price),GROUP_CONCAT(product),GROUP_CONCAT(amount),userEmail,userName FROM stock,data WHERE amount <= warning GROUP BY product,amount,userEmail")
#     cursor.execute(stmt)
#     row = cursor.fetchall()
#     for all in row:
#         currentUser = User(all[4], all[3], "pix")
#         currentProduct = Product(all[1].split(
#             ','), all[2].split(','), all[0].split(','))
#         sendStockAlertMail(currentProduct, currentUser)
#     cursor.close


def addProduct():
    return (True)


def removeProduct():
    return (True)


def editProduct():
    return (True)


def checkStockLimits():
    return (True)


def importStock():
    return (True)
