protocol = new AckProtocol();
client = new WebSocketClient("localhost", "8888", protocol);
dev_list_component = new DeviceListComponent();
protocol.add_component(dev_list_component);
client.connect();