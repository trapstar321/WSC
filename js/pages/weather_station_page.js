protocol = new AckProtocol();
client = new WebSocketClient("localhost", "8888", protocol);
component = new WeatherStationComponent(1);
protocol.add_component(component);
client.connect();