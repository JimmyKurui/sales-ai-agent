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
          <Route path="/agent" element={<DashboardLayout />} />
          
          {/* Protected Sales Agent Routes */}
          <Route
            path="/chat"
            element={
              <ProtectedRoute>
                <ClientChat />
              </ProtectedRoute>
            }
          />
          
          {/* Redirects */}
          <Route path="/" element={<Navigate to="/agent" replace />} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}

export default App
