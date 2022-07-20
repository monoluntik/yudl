import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
import os
import pytube
API_TOKEN = '5318243693:AAHkRa0p3DL03U-bNrCTDPuykPNWJK5SN4Y'

logging.basicConfig(level=logging.INFO)

my_dict = dict()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def try_site(url):
    request = requests.get(url, allow_redirects=False)
    return request.status_code == 200


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nThis bot will help you download video or mp3 file from youtube, for start send me url to video")

@dp.message_handler(lambda message: message.text == "Download as mp3")
async def download_as_mp3(message: types.Message):
    await message.answer('Start downloading, pleas wait')
    yt = pytube.YouTube(my_dict[message.chat.id]).streams.filter(only_audio=True).first()
    yt.download()
    await bot.send_audio(chat_id=message.chat.id, audio=open(yt.default_filename, 'rb'))
    os.remove(yt.default_filename)


@dp.message_handler(lambda message: message.text == "Download as mp4")
async def download_as_mp4(message: types.Message):
    await message.answer('Start downloading, pleas wait')
    yt = pytube.YouTube(my_dict[message.chat.id]).streams.filter(file_extension="mp4").first()
    yt.download()
    await bot.send_video(chat_id=message.chat.id, video=open(yt.default_filename, 'rb'))
    os.remove(yt.default_filename)


@dp.message_handler()
async def send_buttons(message: types.Message):
    if try_site(message.text):
        my_dict[message.chat.id] = message.text
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button_1 = types.KeyboardButton(text="Download as mp3")
        keyboard.add(button_1)
        button_2 = "Download as mp4"
        keyboard.add(button_2)
        await message.answer('Choose format', reply_markup=keyboard)
    else:
        await message.answer('No such vidio')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)