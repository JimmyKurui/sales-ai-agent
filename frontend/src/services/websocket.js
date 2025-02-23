import { io } from "socket.io-client";
import { setConnectionStatus, addMessage, setError } from "../stores/slices/chatSlice";
const BASE_URL = import.meta.env.VITE_API_URL;

class WebSocketService {
    constructor(url) {
      this.url = url;
      this.ws = null;
      this.store = null;
    }
  
    init(store) {
      this.store = store;
      this.connect();
    }
  
    connect() {
      // this.ws = new WebSocket(this.url);
      this.ws = io(this.url, {
        transports: ["websocket"], // Use WebSocket for real-time communication
        reconnection: true, // Enable automatic reconnection
        reconnectionAttempts: 5, // Try 5 times before failing
        reconnectionDelay: 5000, // Wait 5 seconds before retrying
      })
  
      this.ws.onopen = () => {
        this.ws.emit("my_event", function() {
          console.log('My ting')
        });
        this.store.dispatch(setConnectionStatus(true));
      };
  
      this.ws.onclose = () => {
        this.store.dispatch(setConnectionStatus(false));
        setTimeout(() => this.connect(), 5000); // Reconnect after 5 seconds
      };
  
      this.ws.onmessage = (event) => {
        console.log(event.data, typeof event.data)
        
        const message = JSON.parse(event.data);
        this.store.dispatch(addMessage(message));
      };
      this.ws.onerror = (error) => {
        this.store.dispatch(setError('WebSocket error occurred', error));
      };
    }
  
    sendMessage(message) {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(message));
      }
    }
  }
  
  export const wsService = new WebSocketService(`ws://${BASE_URL}`);