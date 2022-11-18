import multiprocessing

from vk import vk_bot
from tg import telegram_bot

if __name__ == '__main__':

    multiprocessing.Process(target=vk_bot.main).start()
    multiprocessing.Process(target=telegram_bot.main).start()

