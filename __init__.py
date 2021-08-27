from hoshino.config import SUPERUSERS
from hoshino import Service, priv
from hoshino.typing import CQEvent
from nonebot import get_bot
import re

from .sql import *
from .api import *
from .draw import *

help = '''
arcinfo 查询b30，需等待1-2分钟
arcre   使用本地查分器查询最近一次游玩成绩
arcre:  指令结尾带：使用est查分器查询最近一次游玩成绩
arcre: arcid  使用好友码查询TA人
arcre: @  使用@ 查询好友
arcup   查询用账号添加完好友，使用该指令绑定查询账号，添加成功即可使用arcre指令
arcbind [arcid] [arcname]   绑定用户
arcun   解除绑定
'''

sv = Service('arcaea', manage_priv=priv.ADMIN, enable_on_default=True, visible=True, help_=help)
asql = arcsql()

@sv.on_prefix(['arcinfo', 'ARCINFO', 'Arcinfo'])
async def arcinfo(bot, ev:CQEvent):
    qqid = ev.user_id
    msg = ev.message.extract_plain_text().strip()
    if 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user(qqid)
    if msg:
        if msg.isdigit() and len(msg) == 9:
            arcid = msg
        else:
            await bot.finish(ev, '仅可以使用好友码查询', at_sender=True)
    elif not result:
        await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
    else:
        arcid = result[0]
    await bot.send(ev, '正在查询，请耐心等待...')
    info = await draw_info(arcid)
    await bot.send(ev, info, at_sender=True)

@sv.on_prefix(['arcre', 'Arcre', 'ARCRE'])
async def arcre(bot, ev:CQEvent):
    qqid = ev.user_id
    est = False
    msg = ev.message.extract_plain_text().strip()
    if 'CQ:at' in str(ev.message):
        result = re.search(r'\[CQ:at,qq=(.*)\]', str(ev.message))
        qqid = int(result.group(1))
    result = asql.get_user(qqid)
    if msg:
        if msg.isdigit() and len(msg) == 9:
            result = asql.get_user_code(msg)
            if not result:
                await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
            user_id = result[0]
        elif msg == ':' or msg == '：':
            if not result:
                await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
            else:
                est = True
                user_id = result[0]
        elif ':' in msg or '：' in msg:
            user_id = msg[1:]
            if user_id.isdigit() and len(user_id) == 9:
                est = True
            else:
                await bot.finish(ev, '请输入正确的好友码', at_sender=True)
        else:
            await bot.finish(ev, '仅可以使用好友码查询', at_sender=True)
    elif not result:
        await bot.finish(ev, '该账号尚未绑定，请输入 arcbind arcid(好友码) arcname(用户名)', at_sender=True)
    elif result[1] == None:
        await bot.finish(ev, '该账号已绑定但尚未添加为好友，请联系BOT管理员添加好友并执行 arcup 指令', at_sender=True)
    else:
        user_id = result[1]
    info = await draw_score(user_id, est)
    await bot.send(ev, info, at_sender=True)

@sv.on_fullmatch(['arcup', 'arcupdate', 'Arcup'])
async def arcup(bot, ev:CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.finish(ev, '请联系BOT管理员更新')
    msg = await newbind()
    await bot.send(ev, msg)

@sv.on_prefix(['arcbind', 'ARCBIND', 'Arcbind'])
async def bind(bot, ev:CQEvent):
    qqid = ev.user_id
    arcid = ev.message.extract_plain_text().strip().split()
    try:
        if not arcid[0].isdigit() and len(arcid[0]) != 9:
            await bot.finish(ev, '请输入您的 arcid(好友码)', at_sender=True)
        elif not arcid[1]:
            await bot.finish(ev, '请输入您的 用户名', at_sender=True)
    except IndexError:
        await bot.finish(ev, '请重新输入好友码和用户名\n例如：arcbind 114514810 sb616', at_sender=True)
    result = asql.get_user(qqid)
    if result:
        await bot.finish(ev, '您已绑定，如需要解绑请输入arcun', at_sender=True)
    msg = await bindinfo(qqid, arcid[0], arcid[1])
    await bot.send(ev, msg, at_sender=True)
    for user_id in SUPERUSERS:
        await get_bot().send_msg(user_id=user_id, message=f'Code:{arcid[0]}\nName:{arcid[1]}\n申请加为好友')

@sv.on_fullmatch(['arcun', 'Arcun', 'ARCUN'])
async def unbind(bot, ev:CQEvent):
    qqid = ev.user_id
    result = asql.get_user(qqid)
    if result:
        if asql.delete_user(qqid):
            msg = '解绑成功'
        else:
            msg = '数据库错误'
    else:
        msg = '您未绑定，无需解绑'
    await bot.send(ev, msg, at_sender=True)
