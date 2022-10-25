from pixqrcode import PixQrCode


def generateQRCode(userPix, city, username, value, clientName):
    pix = PixQrCode(username, userPix, city, value)

    if pix.is_valid():
        pix.save_qrcode(
            "./static/generatedpix", f"pix-{clientName}")
        return pix.generate_code()
    else:
        return "Dados para Pix inválidos."
