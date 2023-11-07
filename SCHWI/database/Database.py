import pymongo
dbclient = pymongo.MongoClient("mongodb+srv://pVbot3seg:segsbot6422pv@cluster0.xzlgp42.mongodb.net/?retryWrites=true&w=majority")
database = dbclient["RESTRICTED"]
user_data = database['allusers']   


groupbase = dbclient["MASSGROUP"]
group_data = groupbase['groupdata']

async def present_group(user_id : int):
    found = group_data.find_one({'_id': int(user_id)})
    return found

async def add_group(user_id: int, admins: list):
    group_data.insert_one(
      {
        '_id': int(user_id),
        'admins': admins
      }
    )
    return

async def del_group(user_id: int):
    group_data.delete_one({'_id': int(user_id)})
    return

async def full_groupbase():
    user_docs = group_data.find()
    group_ids = []
    for doc in user_docs:
        group_ids.append(doc['_id'])
    return group_ids





async def present_user(user_id : int):
    found = user_data.find_one({'_id': int(user_id)})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one(
      {
        '_id': int(user_id),
        'msg': 0
      }
    )
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': int(user_id)})
    return

async def add_ruser_msg(user_id: int):
    user_data.update_one(
        {'_id': int(user_id)},
        {'$inc': {'msg': 1}}
    )

async def get_user(user_id: int):
    Doc = user_data.find_one({'_id': int(user_id)})
    return Doc['msg']


