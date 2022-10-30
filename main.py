import asyncio
import p5.aiogoldsrcrcon
import os

server_address = ('193.19.118.81', 27025)
password = os.environ['rcon_pass']


async def _coroutine():
    async with p5.aiogoldsrcrcon.Connection(address=server_address, password=password) as _connection:
        await _connection.open()

        _response = await _connection.execute(command='status')
        print(_response.strip())


asyncio.get_event_loop().run_until_complete(asyncio.wait_for(_coroutine(), timeout=3))
