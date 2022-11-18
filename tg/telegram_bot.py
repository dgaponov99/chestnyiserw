import logging
import os

from telegram import Update, ForceReply
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from rcon import rcon_connect
from source_query.SourceQuery import SourceQuery
from top import get_top_players_message

from vk.vk_bot import write_msg

emoji_cry = u'\U0001F622'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    print(update.message)
    if update.message.text.lower() == 'сервер':
        try:
            query = SourceQuery('193.19.118.81', 27025)

            s = query.get_server(markdown_v2=True)
            print(s)

            query.disconnect()
            update.message.reply_markdown_v2(s, quote=False)
        except Exception as e:
            print(e)
            s = 'Не могу соединиться с сервером ' + emoji_cry
            update.message.reply_text(s, quote=False)
    elif update.message.text.lower() == 'топ':
        update.message.reply_text(get_top_players_message(), quote=False)
    elif len(update.message.text.strip()) > 5 and update.message.text.lower()[:5] == 'всем:':
        message_to_server = update.message.text[5:].strip()
        try:
            command = 'send_message_rcon "ТГ" "' + update.message.from_user.full_name + '" "' + message_to_server + '"'
            response = rcon_connect.send_command(command)
            print(response)
            write_msg('[ТГ] ' + update.message.from_user.full_name + ': ' + message_to_server)

            # if response:
            #     update.message.reply_text('Сообщение отправлено', quote=True)
        except Exception as e:
            update.message.reply_text('Ошибка при отправке сообщения', quote=True)
            print(e)



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ['tg_token'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    #dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e. message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo, edited_updates=False))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
