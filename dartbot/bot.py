import random
import time
import logging
import os
import logging
import click
from telegram.ext import Updater
from telegram import ChatPermissions
from telegram.ext.filters import Filters, BaseFilter
from telegram.ext import MessageHandler, CommandHandler
from telegram.error import TelegramError


logger = logging.getLogger(__name__)

MUTE_FOR_BULLSEYE = 60 * 60 * 24 * 7


def dart_handler(update, context):
    if update.message.chat.type == 'supergroup':
        member = update.message.chat.get_member(update.message.from_user.id)
        if member.status in ['creator', 'administrator']:
            update.message.reply_text('Ich kann Dich zwar nicht muten, aber sei doch bitte so lieb und halt trotzdem eine Woche lang die Fresse.')
            return
        if member.status == 'left':
            update.message.reply_text('Schade dass Du schon weg bist. Ich werde Deinen Gewinn aufbewahren und einlösen, wenn Du uns wieder besuchst!')
            return
        
        time.sleep(30.0)
        text = random.choice([
            'Jawollo!',
            'Gewinner, Gewinner, Huhn Abendessen!',
            'Viel Spaß bei einer Woche Urlaub von RWTH Informatik!',
            'Endlich'
        ])
        update.message.reply_text(text)
        context.bot.restrict_chat_member(
            update.message.chat.id,
            update.message.from_user.id,
            ChatPermissions(),
            int(time.time() + MUTE_FOR_BULLSEYE))

    else:
        update.message.reply_text('Guter Wurf! Aber jetzt genug geübt, probier dein Glück in der Hauptgruppe!')


def error(update, context):
    """Log Errors caused by Updates."""
    try:
        raise context.error
    except TelegramError as e:
        logger.warning('Update "%s" caused telegram error "%s"', update, e)



def configure_dispatcher(dispatcher):
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(MessageHandler(
        Filters.dice.darts([6]), dart_handler))

@click.command()
@click.option('--bind', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8080)
def cli(bind, port):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    telegram_token = os.environ['BOT_TOKEN']
    updater = Updater(telegram_token, use_context=True)
    configure_dispatcher(updater.dispatcher)
    updater.start_polling()

