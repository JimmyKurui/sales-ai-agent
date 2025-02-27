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
      this.ws = io(this.url, {
        transports: ["websocket"],
        reconnection: true, 
        reconnectionAttempts: 5, 
        reconnectionDelay: 5000, 
      })
      
      this.ws.on("connect", () => {
        this.store.dispatch(setConnectionStatus(true));
      });

      this.ws.on("disconnect", () => {
        this.store.dispatch(setConnectionStatus(false));
      });
  
      this.ws.on("message", (data) => {
        const message = JSON.parse(data);
        this.store.dispatch(addMessage(message));
      });
      
      this.ws.on("error", (error) => {
        this.store.dispatch(setError('WebSocket error occurred', error));
      });
    }
  
    sendMessage(message) {
      if (this.ws?.connected) {
        this.ws.send(JSON.stringify(message));
      }
    }
  }
  
  export const wsService = new WebSocketService(`ws://${BASE_URL}`);