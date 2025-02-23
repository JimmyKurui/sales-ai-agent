import {WebSocketServer} from 'ws';
// server.js
// Create WebSocket server on port 8080
const server = new WebSocketServer({ port: 8080 });

server.on('connection', (stream) => {
  console.log('Client connected');
  stream.on('message', (message) => {
    console.log(`Received message: ${message}, ${typeof message}`);
    server.clients.forEach(function each(client) {
      if (client !== stream && client.readyState == client.OPEN) {
        client.send(message.toString());
      }
    });
  });

  stream.on('close', () => {
    console.log('Client disconnected');
  });

  stream.on('error', (error) => {
    console.error(`WebSocket error: ${error}`);
  });
});

console.log('WebSocket server is running on ws://localhost:8080');
