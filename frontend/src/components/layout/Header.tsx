import React from 'react';
import { NavRoute } from '../../types';
import { Globe, User, ShieldCheck } from 'lucide-react';

interface HeaderProps {
  currentRoute: NavRoute;
  userName: string;
}

export const Header: React.FC<HeaderProps> = ({ currentRoute, userName }) => {
  const getPageTitle = (route: NavRoute) => {
    switch (route) {
      case 'dashboard':
        return {
          title: 'Patient Overview',
          subtitle: 'Voice-guided clinical assessment and medical navigation',
        };
      case 'new-consultation':
        return {
          title: 'Voice Health Consultation',
          subtitle: 'Speak in Hindi, English, or Hinglish to describe your symptoms',
        };
      case 'history':
        return {
          title: 'Consultation Records',
          subtitle: 'Review past clinical symptom assessments and triage reports',
        };
      case 'doctors':
        return {
          title: 'Find Doctors & Specialists',
          subtitle: 'Verified clinicians across Indian cities for in-person or teleconsultation',
        };
      case 'hospitals':
        return {
          title: 'Hospital Network & Emergency Facilities',
          subtitle: 'Verified hospital centers, 24x7 trauma, and ICU facilities across India',
        };
      case 'settings':
        return {
          title: 'Preferences & Safety Settings',
          subtitle: 'Language defaults, emergency contacts, and engine configurations',
        };
      default:
        return {
          title: 'CuraGennie Healthcare',
          subtitle: 'Voice-guided clinical assessment and medical navigation',
        };
    }
  };

  const { title, subtitle } = getPageTitle(currentRoute);

  return (
    <header className="border-b border-ivory-300 bg-ivory-50 px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 className="text-xl font-bold text-forest-900 tracking-tight">{title}</h2>
        <p className="text-xs text-charcoal-700/80 font-normal mt-0.5">{subtitle}</p>
      </div>

      <div className="flex items-center gap-3 self-end sm:self-auto">
        {/* Multilingual Support Pill */}
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-ivory-100 border border-ivory-300 text-xs text-forest-900 font-medium">
          <Globe className="w-3.5 h-3.5 text-sage-600" />
          <span>EN / हिंदी / Hinglish</span>
        </div>

        {/* Security / Non-diagnostic badge */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-sage-50 border border-sage-200 text-xs text-forest-900 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-sage-600" />
          <span>Triage Guidance</span>
        </div>

        {/* User Pill */}
        <div className="flex items-center gap-2 pl-2 border-l border-ivory-300">
          <div className="w-8 h-8 rounded-full bg-forest-800 text-ivory-50 flex items-center justify-center text-xs font-semibold">
            {userName ? userName.charAt(0) : <User className="w-4 h-4" />}
          </div>
          <div className="hidden sm:block text-left">
            <p className="text-xs font-semibold text-forest-900 leading-tight">{userName || 'User'}</p>
            <p className="text-[10px] text-charcoal-700/70">Patient Account</p>
          </div>
        </div>
      </div>
    </header>
  );
};
