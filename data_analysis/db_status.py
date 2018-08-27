from pymongo import MongoClient
from pymongo import WriteConcern
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
import urllib

username = urllib.quote_plus('brgzsqlcommon')
password = urllib.quote_plus('brgzcncs001')
client = MongoClient('mongodb://%s:%s@118.89.50.192:30000/brgz_mixed_cn_cs_001'%(username,password))
db = client.brgz_mixed_cn_cs_001


collection = client.brgz_mixed_cn_cs_001.get_collection(
    'record', write_concern=WriteConcern(w=1, wtimeout=1))

print db.command("dbstats")

for name in db.collection_names():
    print db.get_collection(name)
