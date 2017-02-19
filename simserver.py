import asyncio
import socketio
from aiohttp import web
from life import life


class Simulator(socketio.AsyncNamespace):
    def __init__(self):
        super().__init__()
        self.cells = set()
        self.running = asyncio.Event()
        self.connected_users = 0
        asyncio.ensure_future(self.loop())

    async def on_set_cell(self, sid, cell):
        self.cells.add(tuple(cell))
        await self.draw()

    def on_start(self, sid):
        self.running.set()

    def on_stop(self, sid):
        self.running.clear()

    async def on_connect(self, sid, env):
        self.connected_users += 1
        await self.draw(sid)

    def on_disconnect(self, sid):
        self.connected_users -= 1

    def draw(self, room=None):
        return self.emit("draw", list(self.cells), room=room)

    async def loop(self):
        while await self.running.wait():
            self.cells = life(self.cells)
            await self.draw()
            await asyncio.sleep(1)


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


app = web.Application()
app.router.add_get('/', index)
sio = socketio.AsyncServer()
sio.attach(app)
sio.register_namespace(Simulator())

if __name__ == '__main__':
    web.run_app(app)
