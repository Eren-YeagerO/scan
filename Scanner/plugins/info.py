from pyrogram.types import Message
from pyrogram import filters
from Scanner import pbot as app
from pyrogram.enums.parse_mode import ParseMode

def extract_gban(message):
    hmmm = message.split("-id")[1]
    hmm = hmmm.split("-r")  
    id = int(hmm[0].split()[0].strip())
    reason = hmm[1].split("-p")[0].strip()
    proof = hmm[1].split("-p")[1].strip()
    return id, reason, proof

@app.on_message(filters.command("info"))
@app.on_edited_message(filters.command('info'))
async def info(_,msg:Message):
    m = await msg.reply_text("Searching...")
    if msg.reply_to_message:
        user = msg.reply_to_message.from_user.id

    elif not msg.reply_to_message and len(msg.command) == 1:
        user = msg.from_user.id
        
    elif not msg.reply_to_message and len(msg.command) != 1:
        user = msg.text.split(None, 1)[1]
        
    x = await app.get_users(user)
    z = """User id : <code>{}</code> \nName : {} \nDC id : <code>{}</code>\nPermanent Link : <a href='tg://user?id={}'>{}</a>""".format(x.id,x.first_name,x.dc_id,x.id,x.first_name)
    file = x.photo.big_file_id if x.photo else None
    photo = await app.download_media(file)
    await m.delete()
    await msg.reply_photo(photo,
        caption=z,parse_mode= ParseMode.HTML)
