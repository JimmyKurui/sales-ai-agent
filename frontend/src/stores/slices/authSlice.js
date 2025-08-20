import { createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
// Client login, No Agent auth
const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAuthenticated: false,
    user: null,
    type: null,
    error: null,
  },
  reducers: {
    authenticate: async (state, action) => {
      try {
        const response = await axios.get('/api/agents/login', action.payload);
        state.user = response.data.email;
        state.type = response.data.type;
        setAuth();
      } catch (error) {
        clearAuth();
        setError(error);
      }
    },
    setAuth: (state) => {
      state.isAuthenticated = true;
    },
    clearAuth: (state) => {
      state.isAuthenticated = false;
      state.user = null;
      state.type = null;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const { setAuth, clearAuth, setError, authenticate } = authSlice.actions;
export default authSlice.reducer;