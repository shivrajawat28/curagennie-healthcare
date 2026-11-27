import React, { useState, useEffect } from 'react';
import { NavRoute, DashboardData } from './types';
import { apiService } from './services/api';
import { Navbar } from './components/layout/Navbar';
import { Header } from './components/layout/Header';
import { DisclaimerBanner } from './components/layout/DisclaimerBanner';
import { DashboardView } from './components/dashboard/DashboardView';
import { NewConsultationView } from './components/consultation/NewConsultationView';
import { HistoryView } from './components/history/HistoryView';
import { DoctorsView } from './components/doctors/DoctorsView';
import { SettingsView } from './components/settings/SettingsView';

export const App: React.FC = () => {
  const [currentRoute, setCurrentRoute] = useState<NavRoute>('dashboard');
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(false);

  const fetchInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Check health and retrieve dashboard data concurrently
      const [health, dashboard] = await Promise.all([
        apiService.getHealth().catch(() => null),
        apiService.getDashboard(),
      ]);

      if (health && health.status === 'healthy') {
        setIsBackendHealthy(true);
      } else {
        setIsBackendHealthy(false);
      }

      setDashboardData(dashboard);
    } catch (err: any) {
      console.warn('Backend not yet reachable or returned error:', err);
      setError(
        err.message || 'Unable to connect to CuraGennie backend. Ensure server is running on port 8001.'
      );
      setIsBackendHealthy(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInitialData();
  }, []);

  const renderContent = () => {
    switch (currentRoute) {
      case 'dashboard':
        return (
          <DashboardView
            data={dashboardData}
            loading={loading}
            error={error}
            onRetry={fetchInitialData}
            onNavigate={setCurrentRoute}
          />
        );
      case 'new-consultation':
        return <NewConsultationView onNavigate={setCurrentRoute} />;
      case 'history':
        return <HistoryView onNavigate={setCurrentRoute} />;
      case 'doctors':
        return <DoctorsView onNavigate={setCurrentRoute} />;
      case 'settings':
        return <SettingsView />;
      default:
        return (
          <DashboardView
            data={dashboardData}
            loading={loading}
            error={error}
            onRetry={fetchInitialData}
            onNavigate={setCurrentRoute}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-ivory-50 text-charcoal-800 flex flex-col md:flex-row antialiased selection:bg-sage-100 selection:text-forest-900">
      {/* Sidebar & Mobile Nav */}
      <Navbar
        currentRoute={currentRoute}
        onNavigate={setCurrentRoute}
        isBackendHealthy={isBackendHealthy}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 pb-20 md:pb-6">
        <DisclaimerBanner />
        <Header
          currentRoute={currentRoute}
          userName={dashboardData?.user_name || 'Shiv Rajawat'}
        />
        <main className="flex-1 overflow-y-auto">{renderContent()}</main>
      </div>
    </div>
  );
};

export default App;
