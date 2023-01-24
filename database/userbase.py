import pymongo
import config

myclient = pymongo.MongoClient(config.MONGO_DB_URL)

mydb = myclient[config.MONGO_DB_NAME]
mycol = mydb[config.MONGO_DB_TABLE]

async def getUser(chat_id: int):
    found = mycol.find_one({'_id': chat_id})
    if found:
        return found
    else:
        return False

async def addUser(chat_id: int, namaLengkap: str):
    status = "owner" if config.OWNER_ID == chat_id else "member"
    mycol.insert_one({
        "_id": chat_id,
        "namaLengkap": namaLengkap,
        "status": status,
        "alasan": ""
    })

async def getAll():
    user_id = []
    for doc in mycol.find():
        user_id.append(doc['_id'])
    return user_id

async def updateBan(_id, status, alasan):
    mycol.update_one(
        {"_id": _id},
        {"$set": {
            "status": status,
            "alasan": alasan
        }}
    )