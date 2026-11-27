import React from 'react';
import { DashboardData, NavRoute } from '../../types';
import {
  Mic,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  UserCheck,
  Calendar,
  Sparkles,
  RefreshCw,
  HelpCircle,
  FileText,
} from 'lucide-react';

interface DashboardViewProps {
  data: DashboardData | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  onNavigate: (route: NavRoute) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  data,
  loading,
  error,
  onRetry,
  onNavigate,
}) => {
  if (loading) {
    return (
      <div className="p-8 max-w-6xl mx-auto flex flex-col items-center justify-center min-h-[400px] text-charcoal-700">
        <RefreshCw className="w-8 h-8 animate-spin text-forest-800 mb-3" />
        <p className="text-sm font-medium">Loading clinical dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-6xl mx-auto">
        <div className="p-6 rounded-xl border border-red-200 bg-red-50/60 text-red-900 max-w-xl mx-auto text-center space-y-3">
          <AlertTriangle className="w-10 h-10 text-warmred-600 mx-auto" />
          <h3 className="text-base font-bold">Unable to load dashboard data</h3>
          <p className="text-xs text-charcoal-700 leading-relaxed">{error}</p>
          <button
            onClick={onRetry}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  const stats = data?.stats || {
    total_consultations: 0,
    completed_consultations: 0,
    verified_doctors_available: 18,
    emergency_escalation_ready: true,
  };

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-8">
      {/* Welcome & Primary Voice CTA Hero */}
      <div className="bg-forest-800 text-ivory-50 rounded-2xl p-6 md:p-8 shadow-card relative overflow-hidden">
        <div className="max-w-2xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-forest-900/60 border border-sage-500/30 text-xs text-sage-200">
            <Sparkles className="w-3.5 h-3.5 text-sage-400" />
            <span>Voice-First AI Healthcare Assistant for India</span>
          </div>

          <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-white leading-tight">
            {data?.welcome_message || 'Namaste! How can CuraGennie assist your health today?'}
          </h2>

          <p className="text-sm text-sage-100/90 leading-relaxed">
            Explain symptoms naturally in <strong className="text-white">Hindi</strong>,{' '}
            <strong className="text-white">Hinglish</strong>, or{' '}
            <strong className="text-white">English</strong>. CuraGennie checks for critical warning
            signs, asks clinical follow-up questions, and points you to the right care pathway.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <button
              onClick={() => onNavigate('new-consultation')}
              className="inline-flex items-center gap-2.5 px-5 py-3 rounded-xl bg-sage-200 text-forest-950 font-semibold text-sm hover:bg-white transition-all shadow-soft group"
            >
              <Mic className="w-4 h-4 text-forest-900 group-hover:scale-110 transition-transform" />
              <span>Start Voice Consultation</span>
              <ArrowRight className="w-4 h-4 text-forest-800" />
            </button>

            <button
              onClick={() => onNavigate('doctors')}
              className="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-forest-900/50 hover:bg-forest-900 border border-sage-500/30 text-white font-medium text-sm transition-colors"
            >
              <UserCheck className="w-4 h-4 text-sage-300" />
              <span>Browse Doctors</span>
            </button>
          </div>
        </div>

        {/* Decorative subtle ambient circle */}
        <div className="absolute -right-16 -bottom-16 w-80 h-80 rounded-full bg-sage-500/10 blur-3xl pointer-events-none" />
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white border border-ivory-300 rounded-xl p-4 shadow-soft">
          <p className="text-xs font-medium text-charcoal-700/70">Consultations</p>
          <p className="text-2xl font-bold text-forest-900 mt-1">{stats.total_consultations}</p>
          <p className="text-[11px] text-sage-600 mt-0.5">Recorded assessments</p>
        </div>

        <div className="bg-white border border-ivory-300 rounded-xl p-4 shadow-soft">
          <p className="text-xs font-medium text-charcoal-700/70">Triaged & Completed</p>
          <p className="text-2xl font-bold text-forest-900 mt-1">
            {stats.completed_consultations}
          </p>
          <p className="text-[11px] text-emerald-600 mt-0.5 font-medium">Safe guidance provided</p>
        </div>

        <div className="bg-white border border-ivory-300 rounded-xl p-4 shadow-soft">
          <p className="text-xs font-medium text-charcoal-700/70">Available Doctors</p>
          <p className="text-2xl font-bold text-forest-900 mt-1">
            {stats.verified_doctors_available}
          </p>
          <p className="text-[11px] text-sage-600 mt-0.5">Across major Indian cities</p>
        </div>

        <div className="bg-white border border-ivory-300 rounded-xl p-4 shadow-soft">
          <p className="text-xs font-medium text-charcoal-700/70">Emergency Protocols</p>
          <div className="flex items-center gap-1.5 mt-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <p className="text-base font-bold text-forest-900">Active</p>
          </div>
          <p className="text-[11px] text-charcoal-700/70 mt-0.5">Red-flag interceptors ready</p>
        </div>
      </div>

      {/* Two Column Section: Recent Consultations & Healthcare Guidance */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Recent Consultations List (2 cols on lg) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-forest-900 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-sage-600" />
              <span>Recent Consultations</span>
            </h3>
            <button
              onClick={() => onNavigate('history')}
              className="text-xs font-semibold text-forest-800 hover:text-forest-950 inline-flex items-center gap-1"
            >
              <span>View all</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="space-y-3">
            {data?.recent_consultations && data.recent_consultations.length > 0 ? (
              data.recent_consultations.map((item) => {
                const isMedium = item.risk_level === 'medium';
                const isHigh = item.risk_level === 'high' || item.risk_level === 'emergency';
                return (
                  <div
                    key={item.id}
                    onClick={() => onNavigate('history')}
                    className="p-4 rounded-xl border border-ivory-300 bg-white hover:border-sage-400/80 transition-all cursor-pointer shadow-soft group"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-xs font-semibold text-forest-900">
                            {item.chief_complaint}
                          </span>
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-ivory-100 text-charcoal-700">
                            {item.language}
                          </span>
                        </div>
                        <p className="text-[11px] text-charcoal-700/70">
                          {new Date(item.created_at).toLocaleDateString('en-IN', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </p>
                      </div>

                      <div className="flex flex-col items-end gap-1.5 shrink-0">
                        <span
                          className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${
                            isHigh
                              ? 'bg-red-50 text-red-700 border-red-200'
                              : isMedium
                              ? 'bg-amber-50 text-amber-800 border-amber-200'
                              : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          }`}
                        >
                          {item.risk_level.toUpperCase()} RISK
                        </span>
                        <span className="text-[11px] text-sage-600 font-medium group-hover:underline">
                          View Details →
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="p-8 text-center bg-white rounded-xl border border-ivory-300 space-y-2">
                <FileText className="w-8 h-8 text-sage-400 mx-auto" />
                <p className="text-sm font-semibold text-forest-900">No consultations yet</p>
                <p className="text-xs text-charcoal-700/80">
                  Tap "Start Voice Consultation" to describe your symptoms.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Healthcare Guidance & Voice Tips */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-forest-900 flex items-center gap-2">
              <HelpCircle className="w-4 h-4 text-sage-600" />
              <span>Healthcare Guidance</span>
            </h3>
          </div>

          <div className="space-y-3">
            {data?.guidance_tips.map((tip) => (
              <div
                key={tip.id}
                className="p-4 rounded-xl border border-ivory-300 bg-white shadow-soft space-y-2"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-forest-900">{tip.title}</span>
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-sage-50 text-sage-600 border border-sage-200">
                    {tip.tag}
                  </span>
                </div>
                <p className="text-xs text-charcoal-700/80 leading-relaxed">{tip.summary}</p>
                {tip.action_text && (
                  <button
                    onClick={() => {
                      if (tip.tag === 'Voice Feature') onNavigate('new-consultation');
                      else onNavigate('settings');
                    }}
                    className="text-xs font-semibold text-forest-800 hover:text-forest-950 inline-flex items-center gap-1 pt-1"
                  >
                    <span>{tip.action_text}</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Quick Safety Rule Box */}
          <div className="p-4 rounded-xl bg-ivory-100 border border-ivory-300 text-xs space-y-2">
            <div className="flex items-center gap-1.5 font-semibold text-forest-900">
              <ShieldCheck className="w-4 h-4 text-forest-800" />
              <span>Zero-Key Deterministic Guarantee</span>
            </div>
            <p className="text-charcoal-700/80 leading-relaxed text-[11px]">
              CuraGennie runs with full medical safety without sending your personal symptoms to
              untrusted third parties. Emergency red-flags are caught offline.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
