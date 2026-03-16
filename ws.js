const net = require("net");
const WebSocket = require("ws");

const poolHost = "127.0.0.1";
const poolPort = 8080;

const wss = new WebSocket.Server({ port: 8081 });

wss.on("connection", (ws) => {
  const socket = net.connect(poolPort, poolHost);

  ws.on("message", (msg) => socket.write(msg));
  socket.on("data", (data) => ws.send(data));

  ws.on("close", () => socket.end());
});

console.log("WebSocket proxy running on port 8081");
