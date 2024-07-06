import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import League, TelegramSubscription
from .models import NBAGame
from aiogram import Bot
from django.conf import settings


@receiver(post_save, sender=NBAGame)
def notify_new_game(sender, instance, created, **kwargs):
    if created and instance.status == 'finished':
        league = League.objects.get(name='nba')
        subscribers = TelegramSubscription.objects.filter(league=league)
        for subscription in subscribers:
            user = subscription.user
            if user.telegram_id:
                bot = Bot(token=settings.TELEGRAM_API_KEY)
                message = (
                    f"🏀 NBA Game Finished!\n"
                    f"📅 Date: {instance.date}\n"
                    f"🆚 {instance.visitor_team} - {instance.home_team}\n"
                    f"📊 Score: {instance.visitor_pts} - {instance.home_pts}\n"
                )
                asyncio.run(send_telegram_message(bot, user.telegram_id, message))


async def send_telegram_message(bot, chat_id, message):
    await bot.send_message(chat_id, message)
