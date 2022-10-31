import vk_api
import random
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from source_query import SourceQuery
from utils import get_top_players_message


def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(
        token=os.environ['vk_token'])
    longpoll = VkBotLongPoll(vk_session, 202422455)

    def write_msg(peer_id, message):
        vk_session.method('messages.send',
                          {'peer_id': peer_id, 'random_id': str(random.randint(1, 99999999)), 'message': message})

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
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
                            write_msg(event.object.message['peer_id'], s)
                        except Exception as e:
                            write_msg(event.object.message['peer_id'], 'Не могу соединиться с сервером &#128549;')
                    elif event.object.message['text'].lower() == 'топ':
                        write_msg(event.object.message['peer_id'], get_top_players_message())
        except:
            pass


if __name__ == "__main__":
    main()
