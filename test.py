from source_query import SourceQuery

query = SourceQuery('193.19.118.81', 27025)

s = 'Информация о сервере:\n\n'

# res = query.get_info()
# s += 'Название: ' + res['Hostname'] + '\n'
# s += 'Адрес сервера: 193.19.118.81:27025\n'
# s += 'Карта: ' + res['Map'] + '\n'
# s += 'Онлайн: ' + "%i/%i" % (res['Players'], res['MaxPlayers']) + '\n'

s += '\n'

players = query.get_players()
s += 'Игроки онлайн:\n'
if len(players) > 0:
    for player in players:
        s += "{id}. {Name}, фраги: {Frags}, время: {PrettyTime}".format(**player) + '\n'
else:
    s += 'Сервер пуст :('
print(s)

query.disconnect()
