import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { OfficeMap } from './pages/OfficeMap';
import { Reservations } from './pages/Reservations';
import { ResourceAdmin } from './pages/ResourceAdmin';
import { Dashboard } from './pages/Dashboard';
import type { User } from './types';

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState<string>('map');
  const [selectedResourceIdForBooking, setSelectedResourceIdForBooking] = useState<number | null>(null);

  if (!user) {
    return <Login onLoginSuccess={(u) => setUser(u)} />;
  }

  const handleSelectResourceForBooking = (resourceId: number) => {
    setSelectedResourceIdForBooking(resourceId);
    setActiveTab('reservations');
  };

  return (
    <div className="min-h-screen flex">
      {/* Sidebar Navigation */}
      <Sidebar
        user={user}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onLogout={() => setUser(null)}
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
