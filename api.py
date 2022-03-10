import aiohttp, websockets, json, brotli, os
from typing import Union
from hoshino.log import new_logger

from .sql import asql

api = 'https://webapi.lowiro.com/'
me = 'webapi/user/me'
login = 'auth/login'
est = 'wss://arc.estertion.win:616/'

imgapi = 'http://106.53.138.218:6321/api/'
char_api = 'arcaea/char/'

dir = os.path.join(os.path.dirname(__file__), 'img')
logger = new_logger('Arcaea')

async def get_web_api(email: str, password: str) -> Union[str, dict]:
    data = {'email': email, 'password': password}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api + login, data=data) as req:
                if req.status != 200:
                    return '查询用账号异常，请联系BOT管理员'
            async with session.get(api + me) as reqs:
                return await reqs.json()
    except Exception as e:
        return f'Error {type(e)}'


async def arcb30(arcid: str, re: bool = False) -> Union[str, dict]:
    b30_data = []
    async with websockets.connect(est, timeout=10) as ws:
        await ws.send(str(arcid))
        while True:
            if ws.closed:
                break
            data = await ws.recv()
            if data == 'error,add':
                return '连接查分器错误'
            elif data == 'error,Please update arcaea':
                return '查分器未更新游戏版本'
            elif data == 'error,invalid user code':
                return '好友码无效'
            elif data == 'bye':
                return b30_data
            elif isinstance(data, bytes):
                info = json.loads(brotli.decompress(data))
                if info['cmd'] == 'userinfo' and re:
                    return info
                elif info['cmd'] == 'scores' or info['cmd'] == 'userinfo':
                    b30_data.append(info)

async def update_arc() -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(imgapi + manual_update_api) as req:
                return await req.json()
    except Exception as e:
        return f'Error {type(e)}'
