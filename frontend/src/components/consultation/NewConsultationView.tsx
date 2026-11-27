import React, { useState } from 'react';
import { NavRoute } from '../../types';
import {
  Mic,
  MicOff,
  Globe,
  Sparkles,
  ShieldAlert,
  Send,
  Activity,
} from 'lucide-react';

interface NewConsultationViewProps {
  onNavigate?: (route: NavRoute) => void;
}

export const NewConsultationView: React.FC<NewConsultationViewProps> = () => {
  const [selectedLanguage, setSelectedLanguage] = useState<'hinglish' | 'hi' | 'en'>('hinglish');
  const [inputText, setInputText] = useState('');
  const [isMicSimulated, setIsMicSimulated] = useState(false);

  const samplePrompts = [
    { label: 'Hinglish Fever', text: 'Mujhe 2 din se tez bukhar hai aur badan me dard hai.' },
    { label: 'Chest Discomfort', text: 'Heavy pressure in chest since 20 minutes radiating to left arm.' },
    { label: 'Cough & Throat', text: 'Persistent dry cough for 4 days with throat irritation.' },
    { label: 'Stomach Pain', text: 'Pet me achanak tez dard ho raha hai aur ulti jaisa lag raha hai.' },
  ];

  const handlePromptClick = (text: string) => {
    setInputText(text);
  };

  const handleStartInteraction = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    alert(
      `Phase 01 Scaffold Notice:\n\nInput received: "${inputText}"\nLanguage: ${selectedLanguage}\n\nIn Phase 02, this message will directly enter the Deterministic Medical State Machine and Voice Audio Engine.`
    );
  };

  return (
    <div className="p-6 md:p-8 max-w-4xl mx-auto space-y-6">
      {/* Top Banner Notice */}
      <div className="p-4 rounded-xl border border-sage-200 bg-sage-50/70 flex items-start gap-3">
        <Sparkles className="w-5 h-5 text-forest-800 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h3 className="text-sm font-bold text-forest-900">
            Phase 01 Active — Voice Interface & Intake Shell
          </h3>
          <p className="text-xs text-charcoal-700 leading-relaxed">
            This interface connects the frontend and backend. In Phase 02, browser speech recognition
            (`webkitSpeechRecognition`), canvas waveform, and red-flag triage algorithms will be
            fully wired here.
          </p>
        </div>
      </div>

      {/* Language Selector Bar */}
      <div className="bg-white rounded-xl border border-ivory-300 p-4 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-forest-900">
          <Globe className="w-4 h-4 text-sage-600" />
          <span>Select Consultation Language:</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setSelectedLanguage('hinglish')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              selectedLanguage === 'hinglish'
                ? 'bg-forest-800 text-ivory-50 shadow-soft'
                : 'bg-ivory-100 text-charcoal-700 hover:bg-ivory-200'
            }`}
          >
            Hinglish (Colloquial)
          </button>
          <button
            type="button"
            onClick={() => setSelectedLanguage('hi')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              selectedLanguage === 'hi'
                ? 'bg-forest-800 text-ivory-50 shadow-soft'
                : 'bg-ivory-100 text-charcoal-700 hover:bg-ivory-200'
            }`}
          >
            हिंदी (Hindi)
          </button>
          <button
            type="button"
            onClick={() => setSelectedLanguage('en')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              selectedLanguage === 'en'
                ? 'bg-forest-800 text-ivory-50 shadow-soft'
                : 'bg-ivory-100 text-charcoal-700 hover:bg-ivory-200'
            }`}
          >
            English
          </button>
        </div>
      </div>

      {/* Voice Consultation Centerpiece */}
      <div className="bg-white rounded-2xl border border-ivory-300 p-8 shadow-card text-center space-y-6">
        <div className="max-w-md mx-auto space-y-2">
          <h2 className="text-xl font-bold text-forest-900">Voice-First Symptom Intake</h2>
          <p className="text-xs text-charcoal-700/80">
            Tap the microphone button to dictate or type your concern in plain everyday language.
          </p>
        </div>

        {/* Large Tactile Mic Button */}
        <div className="flex flex-col items-center justify-center py-4">
          <button
            type="button"
            onClick={() => setIsMicSimulated(!isMicSimulated)}
            className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 ${
              isMicSimulated
                ? 'bg-red-500 text-white ring-8 ring-red-100 animate-pulse'
                : 'bg-forest-800 text-ivory-50 hover:bg-forest-900 hover:scale-105 shadow-card'
            }`}
          >
            {isMicSimulated ? <MicOff className="w-10 h-10" /> : <Mic className="w-10 h-10" />}
          </button>

          <p className="text-xs font-semibold text-forest-900 mt-4">
            {isMicSimulated
              ? 'Listening... (Microphone Active - Phase 02 Integration)'
              : 'Tap to speak your symptoms'}
          </p>
          <p className="text-[11px] text-charcoal-700/70 mt-1">
            Web Speech API + Audio Waveform Ready
          </p>
        </div>

        {/* Text Input / Transcript Editor Form */}
        <form onSubmit={handleStartInteraction} className="max-w-2xl mx-auto space-y-3">
          <div className="relative">
            <textarea
              rows={3}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="e.g. 'Mujhe kal raat se sar me dard aur thand lag rahi hai...'"
              className="w-full rounded-xl border border-ivory-300 bg-ivory-50 p-4 text-sm text-charcoal-900 placeholder:text-charcoal-700/40 focus:outline-none focus:ring-2 focus:ring-forest-800 focus:bg-white resize-none"
            />
          </div>

          <div className="flex items-center justify-between gap-3">
            <p className="text-[11px] text-charcoal-700/70 text-left">
              Speak or edit transcript before submitting
            </p>

            <button
              type="submit"
              disabled={!inputText.trim()}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-forest-800 text-ivory-50 font-semibold text-xs hover:bg-forest-900 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              <span>Submit for Triage</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </form>

        {/* Sample Starter Prompts */}
        <div className="pt-4 border-t border-ivory-200">
          <p className="text-xs font-semibold text-forest-900 mb-2 flex items-center justify-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-sage-600" />
            <span>Try sample Indian patient descriptions:</span>
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {samplePrompts.map((prompt) => (
              <button
                key={prompt.label}
                type="button"
                onClick={() => handlePromptClick(prompt.text)}
                className="text-[11px] font-medium px-3 py-1.5 rounded-lg border border-ivory-300 bg-ivory-50 hover:bg-sage-100 hover:border-sage-300 text-charcoal-800 transition-colors"
              >
                {prompt.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Safety Notice Card */}
      <div className="p-4 rounded-xl border border-red-200 bg-red-50/60 text-red-900 text-xs space-y-1.5">
        <div className="flex items-center gap-2 font-bold text-red-800">
          <ShieldAlert className="w-4 h-4 text-warmred-600 shrink-0" />
          <span>Emergency Triage Intercept Notice</span>
        </div>
        <p className="leading-relaxed">
          If at any point your description mentions severe chest tightness, sudden one-sided body
          weakness, inability to breathe, or uncontrollable bleeding, CuraGennie immediately stops
          routine questioning and directs you to emergency hospital facilities (112 / 108).
        </p>
      </div>
    </div>
  );
};
