import logging
import os

#https://api.vk.com/method/messages.send?access_token=vk1.a.0TVflx5sRYme5-buZhMYYoRezDy96ESDxKOBVlTPikEJcN4fyHhst-QZj0IGa_5fBtObTMsnaQTfXKxTqhNIpq2vOc3TAEdV6xuOH16FJYdiBHgkHuH6aBDAJSbTDjPeUGTpFfOhsxR16eiWRqBGQrSkfRvjkRBju9xUkrBd4Gwo11NxNubBwwFOaXcL4aPz7VEdPGi_8nOiQbkJUM6cMw&v=5.131&random_id=8&message=Все знают кто тут главный бот...&peer_id=2000000001
#https://api.telegram.org/bot5691524154:AAGYDE1AxXxeOpffFKmvf_X6zMj4f09JhE0/sendmessage?chat_id=-1001753104086&text=Можно и Игорька на кукан посадить

from telegram import Update, ForceReply, ReplyMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import rcon_connect
from source_query import SourceQuery
from utils import get_top_players_message

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

            s = 'Информация о сервере:\n\n'

            res = query.get_info()
            s += 'Название: *' + res['Hostname'].replace('|', '\\|') + '*\n'
            s += 'Адрес сервера: 193.19.118.81:27025\n'.replace('.', '\\.')
            s += 'Карта: *' + res['Map'].replace('_', '\\_') + '*\n'
            s += 'Онлайн: ' + "%i/%i" % (res['Players'], res['MaxPlayers']) + '\n'

            s += '\n'

            players = query.get_players(escape=True)
            s += 'Игроки онлайн:\n'
            if len(players) > 0:
                for player in players:
                    s += "{id}\\. *{Name}*, фраги: {Frags}, время: {PrettyTime}".format(**player) + '\n'
            else:
                s += 'Сервер пуст ' + emoji_cry
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
