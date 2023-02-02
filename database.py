from pymongo import MongoClient
import certifi


MONGO_URI = 'mongodb+srv://fabian004:Hola123@cluster0.9bekec3.mongodb.net/python'
ca = certifi.where()


def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client['python']
    except ConnectionError:
        print('Error con db')
    return db
