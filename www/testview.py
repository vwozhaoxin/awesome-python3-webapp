from coroweb import get
import asyncio
from models import *
from orm import *

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }



@get('/hello')
async def hello(request):
    return '<h1>hello!</h1>'

