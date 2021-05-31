from configparser import ConfigParser
from termcolor import cprint
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardButton
from lib.word import get_word
import logging
from sys import path as syspath
import json
from time import sleep
# from aiogram.types import InlineQuery, \
#     InputTextMessageContent, InlineQueryResultArticle
# from aiogram.types import InlineKeyboardButton
# from aiogram.types import InlineKeyboardMarkup
# from api import fetch_commands
# from aiogram import types

# Initializing
try:
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config/config.ini')
    API_TOKEN = cfg.get('bot', 'token')
    # AUTH = cfg.get('bot', 'auth')
except Exception as e:
    cprint('Config file error, exit...', 'white', 'on_red')
    # capture_message('Config file error, exit...')
    print(e)
    exit()

try:
    GROUP_CURRENT_WORD = json.load(open("./config/groups.json"))
except Exception as e:
    GROUP_CURRENT_WORD = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
ACT_BUTTON = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
ACT_BUTTON.insert(InlineKeyboardButton(text='🗑️', callback_data='delete'))
ACT_BUTTON.insert(InlineKeyboardButton(text='🚫', callback_data='stop'))


@dp.callback_query_handler(text='delete')
async def _(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(text="该消息已为所有人删除")


@dp.callback_query_handler(text='stop')
async def _(call: types.CallbackQuery):
    # await call.message.delete()
    await call.answer(text="魔鬼教练下班了")


@dp.message_handler(commands=['start', 'welcome', 'about', 'help'])
async def command_start(message: types.Message):
    intro = '''TEST'''
    await bot.send_chat_action(message.chat.id, action="typing")
    await message.answer(intro)


@dp.message_handler(regexp="[A-Za-z'-]+")
async def match(message: types.Message):
    global GROUP_CURRENT_WORD, ACT_BUTTON
    chat_id = str(message.chat.id)
    word = message.text
    if chat_id in GROUP_CURRENT_WORD.keys():
        if word == GROUP_CURRENT_WORD[chat_id][0]:
            index, word, pron, expl = get_word()
            GROUP_CURRENT_WORD[chat_id] = [word, pron, expl]
            json.dump(GROUP_CURRENT_WORD, open("./config/groups.json", 'w'))
            await message.answer("正确！下一个单词是：\n\n**" + pron + "**\n" + expl,
                                 parse_mode='markdown',
                                 disable_notification=True,
                                 disable_web_page_preview=True,
                                 reply_markup=ACT_BUTTON)
            # sleep(10)
            # await message.delete()
        else:
            await message.answer(f"不正确({word})，当前的单词是 " + "\n\n**" +
                                 GROUP_CURRENT_WORD[chat_id][1] + "**\n" +
                                 GROUP_CURRENT_WORD[chat_id][2],
                                 parse_mode='markdown',
                                 disable_notification=True,
                                 disable_web_page_preview=True,
                                 reply_markup=ACT_BUTTON)
            # sleep(10)
            # await message.delete()
    else:
        index, word, pron, expl = get_word()
        GROUP_CURRENT_WORD[chat_id] = [word, pron, expl]
        json.dump(GROUP_CURRENT_WORD, open("./config/groups.json", 'w'))


# @dp.message_handler(content_types=types.message.ContentType.TEXT)
# async def answer(message: types.Message):
#     global GROUP_CURRENT_WORD
#     chat_type = message.chat.type
#     chat_id = message.chat.id
#     action_btn = types.InlineKeyboardMarkup(resize_keyboard=True,
#                                             selective=True)
#     action_btn.insert(InlineKeyboardButton(text='🗑️', callback_data='del'))
#     if chat_type == 'private':
#         await bot.send_chat_action(message.chat.id, action="typing")
#         result = "Success"
#         await message.answer(result, disable_notification=True)
#     elif ((chat_type == 'group') or (chat_type == 'supergroup')):
#         await bot.send_chat_action(message.chat.id, action="typing")
#         index, word, pron, expl = get_word()
#         GROUP_CURRENT_WORD[message.chat.id] = [word, pron]
#         json.dump(GROUP_CURRENT_WORD, open("./config/groups.json", 'w'))
#         await message.answer("**" + word + "**\n" + pron + "\n\n" + expl,
#                              parse_mode='markdown',
#                              disable_notification=True,
#                              disable_web_page_preview=True,
#                              reply_markup=action_btn)
#     else:  # 过滤所有群聊、频道
#         pass


@dp.message_handler(commands=['id'])
async def command_id(message: types.Message):
    global ACT_BUTTON
    await bot.send_chat_action(message.chat.id, action="typing")
    result = message.chat.id
    await message.reply(str(result), reply_markup=ACT_BUTTON)


def exit_gracefully():
    cprint("Current dict saved successfully! Exiting...")


if __name__ == '__main__':
    try:
        cprint('I\'m working now...', 'white', 'on_green')
        executor.start_polling(dp, skip_updates=True)
    except KeyboardInterrupt:
        # print(GROUP_CURRENT_WORD)
        # json.dump(GROUP_CURRENT_WORD, open("./config/groups.json", 'w'))
        pass
    finally:
        # exit_gracefully()
        pass
