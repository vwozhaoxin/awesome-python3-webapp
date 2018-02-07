# -*- coding: utf-8 -*-


#' url handlers '
from models import *
from coroweb import get,post
import re,time,logging,hashlib,base64,asyncio
from models import User, Comment,Blog, next_id

@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }




@get('/hello')
async def hello(request):
    return '<h1>hello!</h1>'

@get('/test')
async def test(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }

@get('/api/users')
async def api_get_users():
   # page_index = get_page_index(page)
   # num = await User.findNumber('count(id)')
  #  p = Page(num, page_index)
   # if num == 0:
   #     return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict( users=users)
