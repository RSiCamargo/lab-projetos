import scripts.cache as ch


def checkClient(key):
    if (ch.load(key) == False):
        return False
    else:
        return True


def clientList():
    clients = ch.loadAll("Client")
    return clients


def findByName(name):
    result = []
    clients = clientList()
    for cl in clients:
        if cl.name.contains(name):
            result.append(cl)

    return result


def delClient(cpf):
    key = "Client_" + cpf.replace('.', '').replace('-', '')
    ch.delete(key)
