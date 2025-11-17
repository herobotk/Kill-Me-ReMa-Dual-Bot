import os
import re
import asyncio
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from filters import FILTERS
from config import API_ID, API_HASH, BOT_TOKEN_1, BOT_TOKEN_2

# Health server
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'alive')

threading.Thread(target=lambda: HTTPServer(("",8080),H).serve_forever(), daemon=True).start()

# BOT1: Filter + Killme (placeholder killme removed for clean demo)
bot1 = Client("bot1", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN_1)

# BOT2: Reply bot
bot2 = Client("bot2", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN_2)

async def send_filter(bot, chat_id, msg_id, data):
    kb = None
    if data.get("buttons"):
        rows=[]
        for row in data["buttons"]:
            rows.append([InlineKeyboardButton(btn["text"], url=btn["url"]) for btn in row])
        kb=InlineKeyboardMarkup(rows)
    if data.get("image"):
        await bot.send_photo(chat_id, data["image"], caption=data.get("text"), reply_to_message_id=msg_id, reply_markup=kb)
    else:
        await bot.send_message(chat_id, data.get("text",""), reply_to_message_id=msg_id, reply_markup=kb)

# BOT1 MANUAL FILTER
@bot1.on_message(filters.group & filters.reply & filters.text)
async def f1(_, m: Message):
    t=m.text.lower().strip()
    if t not in FILTERS: return
    await send_filter(bot1, m.reply_to_message.chat.id, m.reply_to_message.id, FILTERS[t])

@bot1.on_message(filters.group & ~filters.reply & filters.text)
async def f2(_, m: Message):
    t=m.text.lower().strip()
    if t not in FILTERS: return
    await send_filter(bot1, m.chat.id, m.id, FILTERS[t])

# BOT2 REPLY BOT
user_msgs={}
@bot2.on_message(filters.group & filters.text)
async def r1(_, m: Message):
    uid=m.from_user.id if m.from_user else None
    if not uid: return
    now=datetime.utcnow()
    txt=m.text.strip()
    if uid in user_msgs and user_msgs[uid]["text"]==txt and (now-user_msgs[uid]["time"]).seconds<3600:
        sent=await m.reply("Already noted, please wait…")
    else:
        sent=await m.reply("Request received, uploading soon…")
    user_msgs[uid]={"text":txt,"bot_msg_id":sent.id,"time":now}

if __name__=='__main__':
    bot1.start()
    bot2.start()
    asyncio.get_event_loop().run_forever()
