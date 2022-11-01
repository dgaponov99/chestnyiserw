import vk_api
import random
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import rcon_connect
from source_query import SourceQuery
from utils import get_top_players_message

import requests


def telegram_bot_sendtext(bot_message):
    bot_token = os.environ['tg_token']
    bot_chatID = '-1001753104086'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


vk_session = vk_api.VkApi(
    token=os.environ['vk_token'])


def write_msg(message, peer_id=2000000001):
    vk_session.method('messages.send',
                      {'peer_id': peer_id, 'random_id': str(random.randint(1, 4294967295)), 'message': message})


def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    longpoll = VkBotLongPoll(vk_session, 202422455)

    def get_name(id):
        info = getting_api.users.get(user_ids=id)
        print(info)
        full_name = info.get('first_name') + ' ' + info['last_name']
        return full_name

    getting_api = vk_session.get_api()

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    print(event.object.message['text'])
                    if event.object.message['text'].lower() == 'сервер':
                        try:
                            query = SourceQuery('193.19.118.81', 27025)

                            s = 'Информация о сервере:\n\n'

                            res = query.get_info()
                            s += 'Название: ' + res['Hostname'] + '\n'
                            s += 'Адрес сервера: 193.19.118.81:27025\n'
                            s += 'Карта: ' + res['Map'] + '\n'
                            s += 'Онлайн: ' + "%i/%i" % (res['Players'], res['MaxPlayers']) + '\n'

                            s += '\n'

                            players = query.get_players()
                            s += 'Игроки онлайн:\n'
                            if len(players) > 0:
                                for player in players:
                                    s += "{id}. {Name}, фраги: {Frags}, время: {PrettyTime}".format(**player) + '\n'
                            else:
                                s += 'Сервер пуст &#128549;'
                            # print(s)

                            query.disconnect()
                            write_msg(s)
                        except Exception as e:
                            write_msg('Не могу соединиться с сервером &#128549;')
                    elif event.object.message['text'].lower() == 'топ':
                        write_msg(get_top_players_message())
                    elif len(event.object.message['text'].strip()) > 5 and \
                            event.object.message['text'][:5].lower() == 'всем:':
                        print('я тут')
                        message_to_server = event.object.message['text'][5:].strip()
                        print(event.user_id)
                        name = get_name(event.user_id)
                        print('Отправляю сообщение...')
                        try:
                            command = 'send_message_rcon "ТГ" "' + name + '" "' \
                                      + message_to_server + '"'
                            response = rcon_connect.send_command(command)
                            telegram_bot_sendtext('[ВК] ' + name + ': ' + message_to_server)
                            print(response)
                            if response:
                                write_msg(name + ', твое сообщение отправлено')
                        except Exception as e:
                            write_msg(name + ', ошибка, сообщение не отправлено')
                            print(e)
        except:
            pass


if __name__ == "__main__":
    main()
