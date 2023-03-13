import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне название города, а я расскажу какая там погода сейчас \U0001F609")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Мистическая погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind=data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
              f"Погода в городе: {city} \U0001F3D9\nТемпература: {cur_weather}°C \n{wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp} \U0001F305\nЗакат солнца: {sunset_timestamp} \U0001F307\nПродолжительность дня: {length_of_the_day} \U0000231A\n"
              f"\U00002600 Хорошего дня! \U0001F320")

    except:
        await message.reply("Проверьте название города \U00002639")

if __name__ == '__main__':
    executor.start_polling(dp)
