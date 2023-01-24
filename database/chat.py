import pymongo
import config

myclient = pymongo.MongoClient(config.MONGO_DB_URL)

mydb = myclient[config.MONGO_DB_NAME]
mycol = mydb[config.MONGO_DB_TABLE_2]

async def insertMessage(msgID: int, from_user: int, forward_sender_name: str, text: str):
    mycol.insert_one({
        "_id": msgID,
        "from_user": from_user,
        "forward_sender_name": forward_sender_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
        "text": text
    })

async def getMessage(msgID:int):
    found = mycol.find_one({"_id": msgID})
    if found:
        return found
    else:
        return False