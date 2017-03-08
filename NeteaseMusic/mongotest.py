import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Netease']
table = db['netsongs']
d = {'artist':'chou','song':'gaobaiqiqiu','CommentsNum':'123456','url':'http:132.com'}
table.insert(d)
