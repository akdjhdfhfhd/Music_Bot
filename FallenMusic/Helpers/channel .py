# MIT License
#
# Copyright (c) 2023 AnonymousX1025
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from FallenMusic import app
from FallenMusic.utils.database import set_cmode
from FallenMusic.utils.decorators.admins import AdminActual

### Multi-Lang Commands
CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@app.on_message(
    filters.command(CHANNELPLAY_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            _["cplay_1"].format(
                message.chat.title, CHANNELPLAY_COMMAND[0]
            )
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("Channel Play Disabled")
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(
                    chat.linked_chat.title, chat.linked_chat.id
                )
            )
        else:
            return await message.reply_text(_["cplay_2"])
    else:
        try:
            chat = await app.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])
        if chat.type != "channel":
            return await message.reply_text(_["cplay_5"])
        try:
            admins = await app.get_chat_members(
                chat.id, filter="administrators"
            )
        except:
            return await message.reply_text(_["cplay_4"])
        for users in admins:
            if users.status == "creator":
                creatorusername = users.user.username
                creatorid = users.user.id
        if creatorid != message.from_user.id:
            return await message.reply_text(
                _["cplay_6"].format(chat.title, creatorusername)
            )
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(
            _["cplay_3"].format(chat.title, chat.id)
        )
