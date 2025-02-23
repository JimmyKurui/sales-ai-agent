import { setConnectionStatus, addMessage, setError } from "../stores/slices/chatSlice";

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
      this.ws = new WebSocket(this.url);
  
      this.ws.onopen = () => {
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
  
  export const wsService = new WebSocketService('ws://localhost:8080');