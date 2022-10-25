import yagmail


def sendStockAlertMail(product, user):
    app_email = 'labprojetospuc@gmail.com'
    app_password = 'npfyvwfaljvlvplv'  # Token for gmail
    to = user.email

    productList = product.name
    amountList = product.amount
    priceList = product.unitPrice

    list = ""

    for num in range(len(productList)):
        lista = list + \
            f'<span style="border-bottom: 1px solid lightgray;display: inline-block;width: 100%;padding-left:40px"><p style="text-align: left;display: inline-block;width: 70%;">{productList[num]}</p><i>{amountList[num]}</i><a style="text-align: right;display: inline-block;width: 15%;position: relative;">R${priceList[num]}</a></span>'

    subject = 'Alerta de produtos esgotando do estoque'
    content = ['<div style="text-align: center;background-color: #e1e1e1;"><div>',
               f'<h2 style="text-align: center">Olá {user.name},</h2><p style="font-size: large;text-align: center">Este é um email de aviso referente aos produtos que estão acabando de seu estoque. <br> Para adicionar mais no sistema, utilize a mesma template de estoque APENAS com os produtos que irá acrescentar a ele.</p></div><header>',
               yagmail.inline("./static/img/title.png"),
               f'</header><section><article><h1 style="text-align: center">Estoque abaixo do limite</h1><div style="width: 100%;"><a style="width: 65%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Produto</a><a style="width: 12.5%; padding-left: 2.5%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Quantidade</a><a style="width: 9%; padding-left: 1%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Preço(un.)</a></div>',
               lista,
               f'</article></section></div><footer style="margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;text-align: center"><p style="padding: 0px;margin: 5px;">Ward - Automated Billing Service</p><p style="padding: 0px;margin: 5px;">Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p style="padding: 0px;margin: 5px;">Nos contate em labprojetospuc@gmail.com</p></footer></div>']

    with yagmail.SMTP(app_email, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')


def sendBillingMail(qr, client, user, product, total):
    userEmail = 'labprojetospuc@gmail.com'
    app_password = 'npfyvwfaljvlvplv'  # Token for gmail
    to = client.email

    productList = product.name
    amountList = product.amount
    priceList = product.unitPrice
    total = str(total)[:-2]
    virgula = ',00'
    total = total + virgula

    list = ""
    lista = []

    for num in range(len(productList)):
        list = f'<span style="border-bottom: 1px solid lightgray;display: inline-block;width: 100%;padding-left:40px"><p style="text-align: left;display: inline-block;width: 70%;">{productList[num]}</p><i>{amountList[num]}</i><a style="text-align: right;display: inline-block;width: 15%;position: relative;">R${priceList[num]}</a></span>'
        lista.append(list)

    items = ["&emsp;{}".format(s) for s in lista]
    items = "".join(items)
    subject = f'Cobrança à {user.name}'
    content = ['<div style="text-align: center;background-color: #e1e1e1;"><div>',
               f'<h2 style="text-align: center">Olá {client.name},</h2><p style="font-size: large,text-align: center">Este é um email referente à cobrança gerada por {user.name}. Em anexo segue o código pix referente ao valor de R${total}.</p></div>',
               f'<header>',
               yagmail.inline("./static/img/title.png"),
               f'</header><section><article><h1 style="text-align: center">Resumo da compra</h1><div style="width: 100%;"><a style="width: 65%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Produto</a><a style="width: 12.5%; padding-left: 2.5%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Quantidade</a><a style="width: 9%; padding-left: 1%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Preço</a></div>',
               items,
               f'<div style="border-top: 2px solid black"><p style="width: 95%;text-align: right;font-family: sans-serif;font-size: large;font-weight: bold;">Total: R${total}</p></div></article></section></div>',
               yagmail.inline(
                   f"./static/generatedpix/pix-{client.name}.png"),
               '<footer style="margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;text-align: center"><p style="padding: 0px;margin: 5px;">Ward - Automated Billing Service</p><p style="padding: 0px;margin: 5px;">Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p style="padding: 0px;margin: 5px;">Nos contate em labprojetospuc@gmail.com</p></footer></div>']
    attachments = [qr]

    with yagmail.SMTP(userEmail, app_password) as yag:
        yag.send(to, subject, content, attachments)
        print('Sent email successfully')
