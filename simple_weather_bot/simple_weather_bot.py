import logging

from aiogram import Bot, Dispatcher, types # executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import filters
from aiogram.types import Message
from aiogram.utils.executor import start_webhook

import os

import aiohttp

TOKEN = os.environ.get("T_TOKEN", "")
WEBAPP_HOST = "localhost"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_HOST = "https://tento-simple-weather-bot.herokuapp.com" # Change with your host...

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
logger = logging.getLogger(__name__)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
  """This handler receive messages with '/start' command

  :param message: message received
  :type message: Message
  """
  await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")

@dp.message_handler(commands=["id"])
async def command_id_handler(message: Message) -> None:
  await message.answer(f'Your id is {message.chat.id}')

@dp.message_handler(
  filters.RegexpCommandsFilter(regexp_commands=['get\s*([a-zA-Z0-9]+)'])
)
async def command_forecast_handler(message: Message, regexp_command) -> None:
  api_key = os.environ.get("WEATHER_API_KEY", "")
  location = regexp_command.group(1)
  url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      j = await resp.json()
      w: list = j['weather'][0]
      d = w['description']
      reply = f"You have required forecast for {location}"
      reply = f"{reply}\nThe weather in {j['name']} is {d}"
      await message.answer(reply, reply=True)

@dp.message_handler(commands=["get"])
async def command_get_handler(message: Message) -> None:
  await message.answer('Tell me a location to know the weather about', reply=True)

@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
  """
  This handler receive forward message back to the sender

  By default message handler will handle all message types (like text, photo, ...)

  :param message: message received
  :type message: Message
  """
  try:
    await message.send_copy(chat_id=message.chat.id)
  except TypeError:
    await message.answer("Nice try!")

async def on_startup(dp):
  logging.warning("Starting...")
  await bot.set_webhook(WEBHOOK_HOST)
  info = await bot.get_webhook_info()
  logging.info(f"Received info about webhook {info}")

async def on_shutdown(dp):
  logging.warning("Shutting down...")
  await bot.delete_webhook()
  logging.warning("Bye!")

def main() -> None:
  # Uncomment this line to execute in local environment
  # executor.start_polling(dp, skip_updates=True)
  logging.info(f"Running on {WEBHOOK_HOST}:{WEBAPP_PORT}, {WEBAPP_HOST}")
  start_webhook(
    dispatcher=dp,
    webhook_path="/",
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
  )

if __name__ == "__main__":
  main()
