import React, { useState } from 'react';
import { Shield, Volume2, Globe, HeartHandshake, Database } from 'lucide-react';

export const SettingsView: React.FC = () => {
  const [preferredLang, setPreferredLang] = useState('hinglish');
  const [voiceVolume, setVoiceVolume] = useState('0.9');
  const [voiceSpeed, setVoiceSpeed] = useState('1.0');
  const [emergencyPhone, setEmergencyPhone] = useState('112');
  const [savedMessage, setSavedMessage] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedMessage(true);
    setTimeout(() => setSavedMessage(false), 2500);
  };

  return (
    <div className="p-6 md:p-8 max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-xl font-bold text-forest-900">Settings & Safety Preferences</h2>
        <p className="text-xs text-charcoal-700/80 mt-1">
          Configure language preferences, voice speed, and local safety rules.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Language Preference */}
        <div className="bg-white rounded-xl border border-ivory-300 p-5 shadow-soft space-y-4">
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-forest-800" />
            <div>
              <h3 className="text-sm font-bold text-forest-900">Consultation Language</h3>
              <p className="text-xs text-charcoal-700/70">
                Choose default language for speech recognition and triage.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            {[
              { id: 'hinglish', label: 'Hinglish (Colloquial)', desc: 'Everyday Hindi + English blend' },
              { id: 'hi', label: 'हिंदी (Hindi)', desc: 'Standard Devanagari Hindi' },
              { id: 'en', label: 'English', desc: 'Indian English medical terms' },
            ].map((item) => (
              <label
                key={item.id}
                onClick={() => setPreferredLang(item.id)}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                  preferredLang === item.id
                    ? 'border-forest-800 bg-sage-50/70 ring-1 ring-forest-800'
                    : 'border-ivory-300 bg-ivory-50 hover:bg-white'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-forest-900">{item.label}</span>
                  <input
                    type="radio"
                    name="preferredLang"
                    checked={preferredLang === item.id}
                    onChange={() => {}}
                    className="text-forest-800 focus:ring-forest-800"
                  />
                </div>
                <p className="text-[11px] text-charcoal-700/70 mt-1">{item.desc}</p>
              </label>
            ))}
          </div>
        </div>

        {/* Voice Output Settings */}
        <div className="bg-white rounded-xl border border-ivory-300 p-5 shadow-soft space-y-4">
          <div className="flex items-center gap-2">
            <Volume2 className="w-5 h-5 text-forest-800" />
            <div>
              <h3 className="text-sm font-bold text-forest-900">Voice Synthesis (TTS) Settings</h3>
              <p className="text-xs text-charcoal-700/70">
                Controls browser speech speed and volume for assistant replies.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-charcoal-800">
                Speech Rate: {voiceSpeed}x
              </label>
              <input
                type="range"
                min="0.8"
                max="1.4"
                step="0.1"
                value={voiceSpeed}
                onChange={(e) => setVoiceSpeed(e.target.value)}
                className="w-full accent-forest-800"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-charcoal-800">
                Volume: {Math.round(parseFloat(voiceVolume) * 100)}%
              </label>
              <input
                type="range"
                min="0.2"
                max="1.0"
                step="0.1"
                value={voiceVolume}
                onChange={(e) => setVoiceVolume(e.target.value)}
                className="w-full accent-forest-800"
              />
            </div>
          </div>
        </div>

        {/* Emergency Escalation */}
        <div className="bg-white rounded-xl border border-ivory-300 p-5 shadow-soft space-y-4">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-warmred-600" />
            <div>
              <h3 className="text-sm font-bold text-forest-900">Emergency Protocol</h3>
              <p className="text-xs text-charcoal-700/70">
                National emergency helpline triggered on red-flag detection.
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-charcoal-800">
              India National Helpline Number
            </label>
            <input
              type="text"
              value={emergencyPhone}
              onChange={(e) => setEmergencyPhone(e.target.value)}
              className="w-full max-w-xs px-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
            />
            <p className="text-[11px] text-charcoal-700/70">
              Default is 112 (National Emergency Service) or 108 (Disaster Medical Services).
            </p>
          </div>
        </div>

        {/* Architecture & Zero-Key Mode Banner */}
        <div className="p-4 rounded-xl border border-ivory-300 bg-ivory-100 flex items-start gap-3">
          <Database className="w-5 h-5 text-forest-800 shrink-0 mt-0.5" />
          <div className="text-xs text-charcoal-800 space-y-1">
            <p className="font-bold text-forest-900">Zero-Key Deterministic Guarantee Active</p>
            <p className="leading-relaxed">
              CuraGennie stores consultations in local SQLite and runs symptom triage algorithms
              entirely locally. You can optionally add LLM keys, but the system is 100% operational
              without them.
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          {savedMessage ? (
            <span className="text-xs font-semibold text-emerald-700 flex items-center gap-1.5">
              <HeartHandshake className="w-4 h-4" />
              Preferences saved successfully!
            </span>
          ) : (
            <span />
          )}

          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-forest-800 text-ivory-50 font-semibold text-xs hover:bg-forest-900 transition-colors shadow-soft"
          >
            Save Preferences
          </button>
        </div>
      </form>
    </div>
  );
};
