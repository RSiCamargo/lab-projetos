import scripts.cache as ch


def checkClient(key):
    response = ch.load(key)
    return response != False


def clientList():
    clients = ch.loadAll("Client_")
    return clients


def findByName(name):
    result = []
    clients = clientList()
    for cl in clients:
        if cl.name.contains(name):
            result.append(cl)

    return result
