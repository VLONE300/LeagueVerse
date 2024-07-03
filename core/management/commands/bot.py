import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand

from core.utils import nba_slug_team_name, nhl_slug_team_name
from nba.models import NBAGame
from nhl.models import NHLGame

bot = Bot(token=settings.TELEGRAM_API_KEY)

router = Router()
dp = Dispatcher()

button_nba_scores = KeyboardButton(text='NBA')
button_nhl_scores = KeyboardButton(text='NHL')
keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_nba_scores], [button_nhl_scores]],
    resize_keyboard=True,
    one_time_keyboard=False
)


@sync_to_async
def get_nba_scores():
    return list(NBAGame.objects.all()[:5])


@sync_to_async
def get_nhl_scores():
    return list(NHLGame.objects.all()[:5])


@router.message(F.text == 'NBA')
async def show_categories(message: types.Message):
    scores = await get_nba_scores()
    msg_to_answer = ''
    for score in scores:
        visitor_team = await sync_to_async(lambda: score.visitor_team)()
        home_team = await sync_to_async(lambda: score.home_team)()
        visitor_pts = await sync_to_async(lambda: score.visitor_pts)()
        home_pts = await sync_to_async(lambda: score.home_pts)()

        msg_to_answer += (
            f"{nba_slug_team_name[visitor_team.name]}:{visitor_pts} - {nba_slug_team_name[home_team.name]}:{home_pts}\n"
            f'')
    await bot.send_message(message.chat.id, msg_to_answer)


@router.message(F.text == 'NHL')
async def show_categories(message: types.Message):
    scores = await get_nhl_scores()
    msg_to_answer = ''
    for score in scores:
        visitor_team = await sync_to_async(lambda: score.visitor_team)()
        home_team = await sync_to_async(lambda: score.home_team)()
        visitor_pts = await sync_to_async(lambda: score.visitor_pts)()
        home_pts = await sync_to_async(lambda: score.home_pts)()

        msg_to_answer += (
            f"{nhl_slug_team_name[visitor_team.name]}:{visitor_pts} - {nhl_slug_team_name[home_team.name]}:{home_pts}\n"
            f'')
    await bot.send_message(message.chat.id, msg_to_answer)


@router.message(F.text == '/start')
async def command_start(message: types.Message):
    await message.answer(f'Hello {message.from_user.first_name}!', reply_markup=keyboard)


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot for LeagueVerse'

    def handle(self, *args, **options):
        asyncio.run(main())
