const net = require("net");
const WebSocket = require("ws");

const LISTEN_PORT = 9999;
const TCP_HOST = "127.0.0.1";
const TCP_PORT = 1111;

const wss = new WebSocket.Server({ port: LISTEN_PORT });

wss.on("connection", (ws) => {
  console.log("WebSocket client connected");

  const tcp = net.connect(TCP_PORT, TCP_HOST);

  // WS → TCP
  ws.on("message", (msg) => {
    if (tcp.writable) {
      tcp.write(msg);   // send raw buffer
    }
  });

  // TCP → WS
  tcp.on("data", (data) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(data);   // send raw buffer
    }
  });

  ws.on("close", () => {
    tcp.destroy();
    console.log("WebSocket closed");
  });

  tcp.on("close", () => {
    ws.close();
    console.log("TCP closed");
  });

  tcp.on("error", (err) => {
    console.log("TCP error:", err.message);
    ws.close();
  });

  ws.on("error", (err) => {
    console.log("WS error:", err.message);
    tcp.destroy();
  });
});

console.log("WebSocket proxy listening on", LISTEN_PORT);
