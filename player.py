class Player:
    __place_number = None
    __nick = None
    __kills = None
    __deaths = None
    __skill = None

    def __init__(self, place_number, row, sourse='csstats'):
        self.__place_number = int(place_number)
        if sourse == 'csstats':
            self.__csstats_process(row)

    def __csstats_process(self, row):
        self.__nick = row[2]
        self.__kills = int(row[5])
        self.__deaths = int(row[6])
        self.__skill = int(row[4])

    def __str__(self):
        s = ''
        s += str(self.__place_number) + '.'
        s += ' ' + self.__nick + ','
        s += ' фрагов: ' + str(self.__kills) + ','
        s += ' смертей: ' + str(self.__deaths) + ','
        s += ' скилл: ' + str(self.__skill)
        return s
