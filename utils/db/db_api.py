from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

class DatabaseAPI():

    def __init__(self):
        self.uri = "mongodb+srv://birkin:root@clustermaster.oqqyrid.mongodb.net/?retryWrites=true&w=majority"
        self.client = AsyncIOMotorClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client.users
        self.girls_profiles = self.db.profiles_girls
        self.boys_profiles = self.db.profiles_boys
    

    async def get_user(self, user_id: int):
        girl = await self.girls_profiles.find_one({"_id": user_id})
        boy = await self.boys_profiles.find_one({"_id": user_id})
        if girl:
            return girl
        elif boy:
            return boy
    
    
    async def get_girls_profiles(self, user_id: str, viewed: list | None = None):
        if viewed:
            return self.girls_profiles.find({'$and': [{ '$and': [{'_id': {'$nin': viewed}}, {'_id': {'$ne': user_id}}] }, {'$or': [{"prefer_gender": 'boys'}, {"prefer_gender": 'any'}]} ]})
        else:
            return self.girls_profiles.find( { '$and': [ {'_id': {'$ne': user_id}}, {'$or': [{"prefer_gender": 'boys'}, {"prefer_gender": 'any'}]} ] } )

    async def get_boys_profiles(self, user_id: str, viewed: list | None = None):
        if viewed:
            return self.boys_profiles.find({'$and': [{ '$and': [{'_id': {'$nin': viewed}}, {'_id': {'$ne': user_id}}]}, {'$or': [{"prefer_gender": 'girls'}, {"prefer_gender": 'any'}]} ] } )
        else:
            return self.boys_profiles.find( { '$and': [ {'_id': {'$ne': user_id}}, {'$or': [{"prefer_gender": 'girls'}, {"prefer_gender": 'any'}]} ] } )


    async def get_any_profiles(self, user_id: str, viewed: list | None = None):
        if viewed:
            boys = self.boys_profiles.find( { '$and': [{ '$and': [{'_id': {'$nin': viewed}}, {'_id': {'$ne': user_id}}]}, {"prefer_gender": 'any'}]} )
            girls = self.girls_profiles.find( { '$and': [{ '$and': [{'_id': {'$nin': viewed}}, {'_id': {'$ne': user_id}}]}, {"prefer_gender": 'any'}]} )
        else:
            boys = self.boys_profiles.find( { '$and': [ {'_id': {'$ne': user_id}}, {"prefer_gender": 'any'}]} )
            girls = self.girls_profiles.find( { '$and': [ {'_id': {'$ne': user_id}}, {"prefer_gender": 'any'}]} )

        boys_profiles = await boys.to_list(length=20)
        girls_profiles = await girls.to_list(length=20)
        document = []
        if boys_profiles:
            for doc in boys_profiles:
                document.append(doc)
        if girls_profiles:
            for doc in girls_profiles:
                document.append(doc)
        return document

    
    async def set_like(self, from_user_id: str, from_user_username: str, name: str, to_user_id: str, from_gender: str, to_gender: str, action):
        document = {
            'id': from_user_id,
            'username': from_user_username,
            'name': name,
            'gender': from_gender,
            'action': action
        }
        if from_gender == 'boy' and to_gender == 'girl':
            await self.girls_profiles.update_one({"_id": to_user_id}, {'$push': {'like_me': document}})
        elif from_gender == 'girl' and to_gender == 'boy':
            await self.boys_profiles.update_one({"_id": to_user_id}, {'$push': {'like_me': document}})

    async def add_girl_profile(self, user_id: int, username: str, name: str, gender: str):
        
        document = {
            '_id': user_id,
            'username': username,
            'name': name,
            'gender': gender,
            'media': [],
            'like_me': []
        }
        await self.girls_profiles.insert_one(document)


    async def again_girl_profile(self, user_id: int, username: str, gender: str):
        
        document = {
            'username': username,
            'gender': gender,
            'media': []
        }
        await self.girls_profiles.update_one({"_id": user_id}, {'$set': document})

    async def update_girl_media(self, user_id: int, doc: list):
        await self.girls_profiles.update_one({"_id": user_id}, {'$push': {'media': doc}})

    async def clear_girl_media(self, user_id: int):
        await self.girls_profiles.update_one({"_id": user_id}, {'$set': {'media': []}})

    async def update_girl_profile(self, user_id: int, prefer_gender: str, name: str, age: str, city: str, desc: str):
        document = {
            'prefer_gender': prefer_gender,
            "name": name,
            "age": age,
            'city': city,
            'description': desc
        }
        await self.girls_profiles.update_one({"_id": user_id}, {'$set': document})


    async def add_boy_profile(self, user_id: int, username: str, name: str, gender: str):
        
        document = {
            '_id': user_id,
            'username': username,
            'name': name,
            'gender': gender,
            'media': [],
            'like_me': []
        }
        await self.boys_profiles.insert_one(document)

    async def again_boy_profile(self, user_id: int, username: str, gender: str):
        
        document = {
            'username': username,
            'gender': gender,
            'media': []
        }
        await self.boys_profiles.update_one({"_id": user_id}, {'$set': document})

    async def update_boy_media(self, user_id: int, doc: list):
        await self.boys_profiles.update_one({"_id": user_id}, {'$push': {'media': doc}})

    async def clear_boy_media(self, user_id: int):
        await self.boys_profiles.update_one({"_id": user_id}, {'$set': {'media': []}})

    async def update_boy_profile(self, user_id: int, prefer_gender: str, name: str, age: str, city: str, desc: str):

        document = {
            'prefer_gender': prefer_gender,
            "name": name,
            "age": age,
            'city': city,
            'description': desc
        }
        await self.boys_profiles.update_one({"_id": user_id}, {'$set': document})

    




db_API = DatabaseAPI()