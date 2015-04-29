from rpc import server

server = server.Server(1234, 'localhost')
server.run()
