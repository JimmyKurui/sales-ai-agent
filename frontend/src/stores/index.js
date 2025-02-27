import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './slices/chatSlice';
import authReducer from './slices/authSlice';

import { wsService } from '../services/socketio';

const store = configureStore({
  reducer: {
    chat: chatReducer,
    auth: authReducer,
  },
});

wsService.init(store);

export default store;