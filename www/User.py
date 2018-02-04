#*-* coding:utf-8
import orm
from models import User, Blog, Comment
import asyncio

loop = asyncio.get_event_loop()
async def test():
    #await orm.create_pool(user='www-data', password='www-data', db='awesome', loop = loop)
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test1@example.com', passwd='1234567890', image='about:blank',id ="1234")

    await u.save()

loop.run_until_complete(test())


#create instance
#user = User(id=123, name = 'Micheal')
#store data into database
#user.insert({b:123})
#search all users
#user = User.findAll()


