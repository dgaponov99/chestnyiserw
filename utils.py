import my_sql


def get_top_players_message(is_markdown=False):
    players = my_sql.get_top_players()
    message = 'Топ игроков Честного сервера:\n\n'
    if is_markdown or not is_markdown:
        for player in players:
            message += str(player) + '\n'
    return message
