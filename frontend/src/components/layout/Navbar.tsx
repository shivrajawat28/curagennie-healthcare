import React from 'react';
import { NavRoute } from '../../types';
import {
  Activity,
  Mic,
  Clock,
  UserCheck,
  Settings,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';

interface NavbarProps {
  currentRoute: NavRoute;
  onNavigate: (route: NavRoute) => void;
  isBackendHealthy: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentRoute,
  onNavigate,
  isBackendHealthy,
}) => {
  const navItems = [
    { id: 'dashboard' as NavRoute, label: 'Dashboard', icon: Activity },
    { id: 'new-consultation' as NavRoute, label: 'New Consultation', icon: Mic, highlight: true },
    { id: 'history' as NavRoute, label: 'Consultation History', icon: Clock },
    { id: 'doctors' as NavRoute, label: 'Find Doctors', icon: UserCheck },
    { id: 'settings' as NavRoute, label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 border-r border-ivory-300 bg-ivory-100 min-h-screen p-5 shrink-0">
        {/* Brand identity */}
        <div className="flex items-center gap-3 px-2 py-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-forest-800 flex items-center justify-center text-ivory-50 shadow-soft">
            <Activity className="w-5 h-5 text-sage-200" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-forest-900 leading-none">
              Cura<span className="text-sage-500 font-semibold">Gennie</span>
            </h1>
            <p className="text-xs text-charcoal-700/70 mt-1 font-medium">
              Health deserves to be heard
            </p>
          </div>
        </div>

        {/* Primary Navigation */}
        <nav className="space-y-1.5 flex-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentRoute === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors text-left ${
                  isActive
                    ? 'bg-forest-800 text-ivory-50 shadow-soft'
                    : item.highlight
                    ? 'bg-sage-100 text-forest-900 hover:bg-sage-200/80'
                    : 'text-charcoal-700 hover:bg-ivory-200/60 hover:text-forest-900'
                }`}
              >
                <Icon
                  className={`w-4 h-4 ${
                    isActive
                      ? 'text-sage-200'
                      : item.highlight
                      ? 'text-forest-800'
                      : 'text-sage-600'
                  }`}
                />
                <span>{item.label}</span>
                {item.highlight && !isActive && (
                  <span className="ml-auto text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-sage-200 text-forest-900">
                    Voice
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* System & Emergency Status Card */}
        <div className="mt-auto pt-4 space-y-3">
          <div className="p-3 rounded-lg border border-ivory-300 bg-ivory-50 text-xs space-y-2">
            <div className="flex items-center justify-between text-charcoal-700 font-medium">
              <span className="flex items-center gap-1.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    isBackendHealthy ? 'bg-emerald-500 ring-2 ring-emerald-100' : 'bg-amber-500'
                  }`}
                />
                Engine Status
              </span>
              <span className="text-[11px] text-sage-600 font-semibold uppercase">
                {isBackendHealthy ? 'Local Offline' : 'Connecting'}
              </span>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-charcoal-700/80">
              <Sparkles className="w-3.5 h-3.5 text-sage-500 shrink-0" />
              <span>Zero-key triage ready</span>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-red-50/70 border border-red-100 text-xs text-warmred-600 space-y-1">
            <div className="flex items-center gap-1.5 font-semibold text-red-700">
              <ShieldAlert className="w-3.5 h-3.5 shrink-0" />
              <span>Emergency Help</span>
            </div>
            <p className="text-[11px] text-red-700/80 leading-relaxed">
              In acute life threat, dial <strong className="font-bold underline">112</strong> or{' '}
              <strong className="font-bold underline">108</strong> immediately.
            </p>
          </div>
        </div>
      </aside>

      {/* Mobile Top Header + Bottom Navigation Bar */}
      <header className="md:hidden sticky top-0 z-40 bg-ivory-100 border-b border-ivory-300 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-forest-800 flex items-center justify-center text-ivory-50">
            <Activity className="w-4 h-4 text-sage-200" />
          </div>
          <span className="font-bold text-forest-900 tracking-tight">CuraGennie</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              isBackendHealthy ? 'bg-emerald-500' : 'bg-amber-500'
            }`}
          />
          <span className="text-xs font-medium text-charcoal-700">Zero-Key</span>
        </div>
      </header>

      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-ivory-100 border-t border-ivory-300 px-2 py-2 flex items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentRoute === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`flex flex-col items-center gap-1 py-1 px-2.5 rounded-lg text-[10px] font-medium transition-colors ${
                isActive
                  ? 'text-forest-900 font-bold'
                  : 'text-charcoal-700 hover:text-forest-800'
              }`}
            >
              <div
                className={`p-1.5 rounded-md ${
                  isActive
                    ? 'bg-forest-800 text-ivory-50'
                    : item.highlight
                    ? 'bg-sage-100 text-forest-800'
                    : 'text-sage-600'
                }`}
              >
                <Icon className="w-4 h-4" />
              </div>
              <span className="truncate max-w-[58px]">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </>
  );
};
