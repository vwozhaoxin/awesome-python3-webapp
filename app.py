# *-* config:utf-8 *-*
#author xin zhao

import logging;logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time, aiomysql
from datetime import datetime

from aiohttp import web
from  www.orm import Model, StringField, IntegerField

class User(Model):

    __table__ = 'user'
    id = IntegerField(primary_key=True)
    name = StringField()



def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', headers={'content-type':'text/html'})


async def init(loop):
    app = web.Application(loop= loop)
    app.router.add_route('GET','/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
    logging.info('create database connection pool ...')
    global __pool
    __pool = await  aiomysql .create_pool(
    host = kw.get('host', 'localhost'),
    port = kw.get('port', '3306'),
    user = kw['user'],
    password = kw['password'],
    db = kw['db'],
    charset = kw.get('charset', 'utf8'),
    autocommit = kw.get('autocommit', True),
    maxsize = kw.get('maxsize', 10),
    minsize = kw.get('minsize', 1)  ,
    loop = loop
    )
async def select(sql, args, size = None):
    log(sql, args)
    global __pool
    async with __pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?',"%s"), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()

        logging.info('rows returned: %s' % len(rs))
        return rs

async def execute(sql, args, autocommit = True):
    log(sql)
    async with __pool.acquire() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql.replace('?', '%s'),args)
                    affected =cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected



loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool(host='127.0.0.1', port=3306,user='root', password='password',db='test', loop=loop))
rs = loop.run_until_complete(select('select * from runoob_tbl',None))
#rs = loop.run_until_complete(execute('insert ('haha','shenmegui', NOW()) into runnoob_tb1)
print("heh:%s" % rs)