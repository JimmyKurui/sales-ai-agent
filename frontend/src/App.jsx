import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import store from './stores/index';
import ProtectedRoute from './router/ProtectedRoute';

import DashboardLayout from './layouts/DashboardLayout'; 
import ClientChat from './views/ClientChat';
import LoginPage from './pages/LoginPage';

function App() {

  return (
    <Provider store={store}>
       <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/chat" element={<ClientChat />} />
          
          {/* Protected Sales Agent Routes */}
          <Route
            path="/agent/*"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          />
          
          {/* Redirects */}
          <Route path="/" element={<Navigate to="/chat" replace />} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}

export default App
