from pixqrcode import PixQrCode


def generateQRCode(user, clientName, value):
    pix = PixQrCode(user.name, user.tel, user.city, value)

    if pix.is_valid():
        pix.save_qrcode(
            "./static/generatedpix", f"pix-{clientName}")
        return pix.generate_code()
    else:
        return "Dados para Pix inválidos."
