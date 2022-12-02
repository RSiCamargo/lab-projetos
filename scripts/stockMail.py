import scripts.stock as st
import scripts.cache as ch
import yagmail

# labprojetostestes@gmail.com
# senhalabprojetos


def checkStockStatus():
    products = st.productList()
    user = ch.load("User_key")

    sysMail = 'labprojetostestes@gmail.com'
    app_password = 'qtlprqhrqwgtzpch'  # Token for gmail

    productList = []
    qntList = []
    alertList = []

    for product in products:
        if (int(product.qnt) <= int(product.alert)):
            productList.append(product.product)
            qntList.append(product.qnt)
            alertList.append(product.alert)

    list = ""
    lista = []

    for num in range(len(productList)):
        list = f'<span style="border-bottom: 1px solid lightgray;display: inline-block;width: 100%;padding-left:40px"><p style="text-align: left;display: inline-block;width: 70%;">{productList[num]}</p><i>{qntList[num]} un.</i><a style="text-align: right;display: inline-block;width: 15%;position: relative;">{alertList[num]} un.</a></span>'
        lista.append(list)

    items = ["&emsp;{}".format(s) for s in lista]
    items = "".join(items)
    subject = f'{"WARD - Alerta de produtos acabando no estoque."}'
    content = ['<div style="text-align: center;background-color: #e1e1e1;"><div>',
               f'<h2>Olá {user.name},</h2><p style="font-size: large">Este é um email de aviso referente aos produtos que estão acabando de seu estoque. <br> Para adicionar mais no sistema, acesse a plataforma. <br> Lembramos que ao adicionar o mesmo produto com valores de custo, repasse e alerta diferente dos existentes, os valores serão atualizados, porém a quantidade será apenas adicionada.</p></div>',
               f'<div style="border: solid 1px gray; width: 1000px; margin: 0 auto; background-color: white; box-shadow: 2px 2px #86868621"><header>',
               yagmail.inline("./static/img/title.png"),
               f'</header><section><article><h1 style="text-align: center">Resumo da compra</h1><div style="width: 100%;"><a style="width: 65%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Produto</a><a style="width: 12.5%; padding-left: 2.5%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Quantidade</a><a style="width: 9%; padding-left: 3%;display: inline-block;position: relative;font-weight: bold;text-align: left;">Qnt Alerta</a></div>',
               items,
               '<footer style="margin-top: 10px;color: rgb(143, 143, 143);font-family: sans-serif;text-align: center"><p style="padding: 0px;margin: 5px;">Ward - Automated Billing Service</p><p style="padding: 0px;margin: 5px;">Av. Padre Cletus Francis Cox, 1661 - Country Club, Poços de Caldas - MG, 37714-620</p><p style="padding: 0px;margin: 5px;">Nos contate em labprojetospuc@gmail.com</p></footer></div>']

    with yagmail.SMTP(sysMail, app_password) as yag:
        yag.send(user.email, subject, content)
        print('Sent billing email successfully')
