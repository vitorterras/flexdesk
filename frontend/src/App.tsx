import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { OfficeMap } from './pages/OfficeMap';
import { Reservations } from './pages/Reservations';
import { ResourceAdmin } from './pages/ResourceAdmin';
import { Dashboard } from './pages/Dashboard';
import type { User } from './types';

export function App() {
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem('flexdesk_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [activeTab, setActiveTab] = useState<string>(() => {
    return localStorage.getItem('flexdesk_tab') || 'map';
  });

  const [selectedResourceIdForBooking, setSelectedResourceIdForBooking] = useState<number | null>(null);

  const handleLoginSuccess = (u: User) => {
    setUser(u);
    localStorage.setItem('flexdesk_user', JSON.stringify(u));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('flexdesk_user');
    localStorage.removeItem('flexdesk_tab');
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    localStorage.setItem('flexdesk_tab', tab);
  };

  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  const handleSelectResourceForBooking = (resourceId: number) => {
    setSelectedResourceIdForBooking(resourceId);
    handleTabChange('reservations');
  };

  return (
    <div className="min-h-screen flex">
      {/* Sidebar Navigation */}
      <Sidebar
        user={user}
        activeTab={activeTab}
        setActiveTab={handleTabChange}
        onLogout={handleLogout}
      />

      {/* Main Content Area */}
      <main className="flex-1 ml-72 p-8 max-w-7xl">
        {activeTab === 'map' && (
          <OfficeMap user={user} onSelectResourceForBooking={handleSelectResourceForBooking} />
        )}
        {activeTab === 'reservations' && (
          <Reservations user={user} initialSelectedResourceId={selectedResourceIdForBooking} />
        )}
        {activeTab === 'admin' && user.perfil_id === 2 && <ResourceAdmin />}
        {activeTab === 'dashboard' && user.perfil_id === 2 && <Dashboard />}
      </main>
    </div>
  );
}

export default App;
