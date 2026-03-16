const net = require("net");
const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 9999 });

wss.on("connection", (ws) => {
  const tcp = net.connect(8080, "127.0.0.1");

  ws.on("message", (msg) => {
    tcp.write(msg);
  });

  tcp.on("data", (data) => {
    ws.send(data.toString());
  });
});
