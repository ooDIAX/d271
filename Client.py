import asyncio
import aioconsole

class ChatClient:
    def __init__(self, name):
        self.name = name

    # read messages from the server and print them to the console
    async def receive_messages(self, reader):
        while True:
            # print("Waiting for message")
            message = await reader.readline()
            # print("Message received")
            if not message:
                break
            print(message.decode().rstrip())


    # read messages from the user and send them to the server
    async def send_messages(self, writer):
        while True:
            message = await aioconsole.ainput()

            # print(f'Sending: {message}')
            writer.write((message + "\n").encode())
            # writer.write_eof()
            await writer.drain()


    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection('localhost', 8888)
        self.writer.write(self.name.encode())
        await self.writer.drain()

        # get event loop
        loop = asyncio.get_event_loop()

        t2 = asyncio.create_task(self.receive_messages(self.reader))
        t1 = asyncio.create_task(self.send_messages(self.writer))

        await asyncio.gather(t1, t2)

if __name__ == '__main__':
    name = input('Enter your name: ')
    client = ChatClient(name)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        pass

    loop.close()
