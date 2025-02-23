import { createSlice } from '@reduxjs/toolkit';

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    isConnected: false,
    activeConversation: null,
    error: null,
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setConnectionStatus: (state, action) => {
      state.isConnected = action.payload;
    },
    setActiveConversation: (state, action) => {
      state.activeConversation = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const { addMessage, setConnectionStatus, setActiveConversation, setError } = chatSlice.actions;
export default chatSlice.reducer;