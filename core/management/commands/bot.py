import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F
from django.conf import settings
from django.core.management.base import BaseCommand

bot = Bot(token=settings.TELEGRAM_API_KEY)

router = Router()
dp = Dispatcher()


@router.message(F.text == '/start')
async def command_start(message: types.Message):
    await message.answer('Hello!')


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot for LeagueVerse'

    def handle(self, *args, **options):
        asyncio.run(main())
