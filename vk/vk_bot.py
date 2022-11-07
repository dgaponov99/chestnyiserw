import vk_api
import random
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from rcon import rcon_connect
from source_query.SourceQuery import SourceQuery
from top import get_top_players_message

import requests

from vk import vk_session


def telegram_bot_sendtext(bot_message):
    bot_token = os.environ['tg_token']
    bot_chatID = '-1001753104086'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()




def write_msg(message, peer_id=2000000001):
    vk_session.method('messages.send',
                      {'peer_id': peer_id, 'random_id': str(random.randint(1, 4294967295)), 'message': message})


def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    longpoll = VkBotLongPoll(vk_session, 202422455)

    def get_name(id):
        info = getting_api.users.get(user_ids=id)[0]
        print(info)
        return info.get('first_name'), info['last_name']

    getting_api = vk_session.get_api()

    # todo: need callback
    while True:
        try:
            for event in longpoll.listen():
                try:
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        print(event)

                        if event.object.message['peer_id'] != 2000000001:
                            continue

                        print(event.object.message['text'])
                        if event.object.message['text'].lower() == 'сервер':
                            try:
                                query = SourceQuery('193.19.118.81', 27025)
                                s = query.get_server()
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
                            name, lastname = get_name(event.object.message['from_id'])
                            print(name)
                            print('Отправляю сообщение...')
                            try:
                                command = 'send_message_rcon "ВК" "' + name + ' ' + lastname + '" "' \
                                          + message_to_server + '"'
                                response = rcon_connect.send_command(command)
                                telegram_bot_sendtext('\\[ВК] ' + name + ' ' + lastname + ': ' + message_to_server)
                                print(response)
                                if response:
                                    write_msg(name + ', твое сообщение отправлено')
                            except Exception as e:
                                write_msg(name + ', ошибка, сообщение не отправлено')
                                print(e)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
