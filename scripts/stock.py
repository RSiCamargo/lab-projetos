# add product
# remove product
# edit product quantity
# edit product price
# check stock after something is used (alert if below limit)

import scripts.cache as ch


def checkProduct(key):
    if (ch.load(key) == False):
        return False
    else:
        return True


def delProduct(name):
    key = "Product_" + name
    ch.delete(key)


def productList():
    products = ch.loadAll("Product")
    return products


def checkStockLimits():
    return (True)
