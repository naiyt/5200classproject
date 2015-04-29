from rpc.factory import Factory

factory = Factory()
server = factory.get_proxy()
server.connect()
print server.subtract(1, 2) + server.add(1, 2)
