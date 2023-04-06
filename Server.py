import asyncio
import os

class ChatServer:
    def __init__(self):
        self.clients = {}

    async def handle_client(self, reader, writer):
        # Get the client's name
        name = (await reader.read(100)).decode()
        print(f'New client connected: {name}')
        self.clients[name] = writer

        # Listen for messages from the client and broadcast them to all other clients
        path = os.path.abspath(__file__)
        path = path[:-14]
        while True:
            message = (await reader.read(100)).decode()
            if not message:
                break

            print(f'{name}: {message}')
            # for client_name, client_writer in self.clients.items():
            #     if client_name != name:
            #         print(f"Sending to {client_name}")
            #         client_writer.write(f'{name}: {message}'.encode())
            #         await client_writer.drain()
            #         print(f"Sent to {client_name}")

            print(message.split()[0])
            print(message.split())


            if(message == "list\n"):
                print(f"Sending to {name}")

                dir_list = os.listdir(path)
                dirs = ""

                print(path)
                for dir in dir_list:
                    print(dir)
                    dirs += "> " + dir + "\n"
                self.clients[name].write(f'{dirs}'.encode())
            
                await self.clients[name].drain()
                print(f"Sent to {name}")
            elif(message.split()[0] == "cd"):
                
                print(f"Sending to {name}")

                if(os.path.exists(message.split()[1])):
                    path = message.split()[1]
                    mssg = 'OK'
                else:
                    mssg = 'Enter correct path'

                mssg += "\n"
                self.clients[name].write(f'> {mssg}'.encode())
                await self.clients[name].drain()
                print(f"Sent to {name}")
            elif(message.split()[0] == "get"):
                print(f"Sending to {name}")

                try:
                    f = open(path + "\\" + message.split()[1], "r")
                    
                    lines = ""
                    for line in f.readlines():
                        print(line + "--")
                        lines += "> " + line
                    self.clients[name].write(f'{lines}\n'.encode())
                    await self.clients[name].drain()
                except:
                    self.clients[name].write(f'File doesn\'t exist or isn\'t executable \n'.encode())
                    await self.clients[name].drain()

                # if(os.path.exists(path + "\\" + message.split()[1])):
                #     f = open(path + "\\" + message.split()[1], "r")

                #     print(f.read())
                #     self.clients[name].write(f'{f.read()}\n'.encode())
                #     await self.clients[name].drain()

                #     f.close()
                # else:
                #     self.clients[name].write(f'No such file\n'.encode())
                #     await self.clients[name].drain()
                    
                print(f"Sent to {name}")    

            else:
                print(f"Sending to {name}")
                self.clients[name].write(f'> Enter correct command \n'.encode())
                await self.clients[name].drain()
                print(f"Sent to {name}")


        # Remove the client from the list of connected clients
        del self.clients[name]
        print(f'Client disconnected: {name}')

    async def start(self):
        
        server = await asyncio.start_server(self.handle_client, 'localhost', 8888)

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    print("code executed")
    chat_server = ChatServer()
    asyncio.run(chat_server.start())
