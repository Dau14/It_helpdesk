import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import TicketForm from './components/TicketForm';
import TicketList from './components/TicketList';
import AdminPanel from './components/AdminPanel';
import AssetForm from './components/AssetForm';
import AssetList from './components/AssetList';
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (newToken, userRole) => {
    setToken(newToken);
    setRole(userRole);
  };

  useEffect(() => {
    if (token) {
      const ws = new WebSocket('ws://localhost:8000/ws');
      ws.onmessage = (event) => {
        alert(`Notification: ${event.data}`);
      };
      return () => ws.close();
    }
  }, [token]);

  return (
    <div>
      <h1>IT Helpdesk System</h1>
      {!token ? (
        <>
          {showRegister ? <Register onRegister={() => setShowRegister(false)} /> : <Login onLogin={handleLogin} />}
          <button onClick={() => setShowRegister(!showRegister)}>
            {showRegister ? 'Back to Login' : 'Register'}
          </button>
        </>
      ) : (
        <>
          <TicketForm token={token} />
          <TicketList token={token} role={role} />
          {role === 'admin' && (
            <>
              <AdminPanel token={token} />
              <AssetForm token={token} />
              <AssetList token={token} />
              <Dashboard token={token} />
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;