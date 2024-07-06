import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import League, TelegramSubscription
from users.models import TelegramUser

bot = Bot(token=settings.TELEGRAM_API_KEY)
router = Router()
dp = Dispatcher()


def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Subscribe to NBA", callback_data='subscribe_nba')],
        [InlineKeyboardButton(text="Subscribe to NHL", callback_data='subscribe_nhl')]
    ])
    return keyboard


@router.message(F.text == '/start')
async def start(message: types.Message):
    keyboard = get_subscription_keyboard()
    await message.answer("Choose a league to subscribe:", reply_markup=keyboard)


@router.callback_query(F.data.startswith('subscribe_'))
async def process_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    league_name = callback_query.data.split('_')[1]

    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(telegram_id=user_id, )

    try:
        league = await sync_to_async(League.objects.get)(name=league_name)
    except League.DoesNotExist:
        await bot.send_message(callback_query.from_user.id, f"League {league_name} does not exist.")
        await callback_query.answer()
        return

    subscription, created = await sync_to_async(TelegramSubscription.objects.get_or_create)(user=user, league=league)

    if created:
        await bot.send_message(callback_query.from_user.id,
                               f"You have successfully subscribed to {league_name} notifications.")
    else:
        await bot.send_message(callback_query.from_user.id,
                               f"You are already subscribed to {league_name} notifications.")

    await callback_query.answer()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot for LeagueVerse'

    def handle(self, *args, **options):
        asyncio.run(main())
