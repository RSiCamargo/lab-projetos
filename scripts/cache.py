from sqlitedict import SqliteDict


def save(key, value, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value
            mydict.commit()
    except Exception as ex:
        print("Erro durante salvamento de dados: ", ex)


def load(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            value = mydict[key]
        return value
    except Exception as ex:
        print("Erro durante carregamento de dados: ", ex)
        return False


def loadAll(catKey, cache_file="cache.sqlite3"):
    ret = []
    try:
        with SqliteDict(cache_file) as mydict:
            for key in mydict.keys():
                if catKey in key:
                    ret.append(mydict[key])
        return ret
    except Exception as ex:
        print("Erro durante carregamento de dados: ", ex)
        return False


def delete(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict.pop(key)
            mydict.commit()
    except Exception as ex:
        print("Erro durante exclusao de dados: ", ex)
