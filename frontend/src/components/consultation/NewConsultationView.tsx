import React, { useState, useEffect, useRef } from 'react';
import {
  NavRoute,
  EngineResponse,
  AssessmentResponse,
  QuestionDetail,
  SafetyStatus,
} from '../../types';
import { apiService } from '../../services/api';
import {
  Globe,
  Send,
  ShieldAlert,
  AlertTriangle,
  CheckCircle,
  RefreshCw,
  PhoneCall,
  Activity,
  User,
  RotateCcw,
  Sparkles,
  ArrowRight,
  FileText,
} from 'lucide-react';

interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  time: string;
}

interface NewConsultationViewProps {
  onNavigate?: (route: NavRoute) => void;
}

export const NewConsultationView: React.FC<NewConsultationViewProps> = ({ onNavigate }) => {
  const [selectedLanguage, setSelectedLanguage] = useState<'hinglish' | 'hi' | 'en'>('hinglish');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionError, setSessionError] = useState<string | null>(null);

  const [currentQuestion, setCurrentQuestion] = useState<QuestionDetail | null>(null);
  const [safetyStatus, setSafetyStatus] = useState<SafetyStatus | null>(null);
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [isComplete, setIsComplete] = useState(false);

  const chatBottomRef = useRef<HTMLDivElement>(null);

  // Initialize a consultation session on mount or language switch
  const initializeSession = async (lang: 'hinglish' | 'hi' | 'en') => {
    setLoading(true);
    setSessionError(null);
    setAssessment(null);
    setIsComplete(false);
    setCurrentQuestion(null);
    setSafetyStatus(null);
    try {
      const res: EngineResponse = await apiService.startConsultation(lang);
      setSessionId(res.session_id);
      setMessages([
        {
          id: 'welcome-' + Date.now(),
          role: 'assistant',
          content: res.assistant_message,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
      setSafetyStatus(res.safety_status);
      setCurrentQuestion(res.next_question || null);
    } catch (err: any) {
      setSessionError(err.message || 'Failed to initialize consultation session with backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initializeSession(selectedLanguage);
  }, [selectedLanguage]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || !sessionId || loading) return;

    // Add user message to UI immediately
    const userMsg: ChatMessage = {
      id: 'user-' + Date.now(),
      role: 'user',
      content: text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);
    setSessionError(null);

    try {
      const res: EngineResponse = await apiService.sendMessage(sessionId, text);

      // Add assistant reply to UI
      const asstMsg: ChatMessage = {
        id: 'asst-' + Date.now(),
        role: 'assistant',
        content: res.assistant_message,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, asstMsg]);
      setCurrentQuestion(res.next_question || null);
      setSafetyStatus(res.safety_status);
      if (res.assessment) {
        setAssessment(res.assessment);
      }
      setIsComplete(res.is_complete || res.state === 'ESCALATED' || res.state === 'COMPLETED');
    } catch (err: any) {
      setSessionError(err.message || 'Error communicating with healthcare conversation engine.');
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    { label: 'Hinglish Fever & Body Ache', text: 'Mujhe 2 din se tez bukhar hai aur badan me dard hai' },
    { label: 'Chest Pressure (Emergency)', text: 'Severe crushing chest pain radiating to left arm and sweating' },
    { label: 'English Dry Cough', text: 'I have a dry cough and throat irritation since 4 days' },
    { label: 'Abdominal Cramping (Hinglish)', text: 'Pet me achanak tez dard aur ulti jaisa lag raha hai' },
  ];

  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto space-y-6">
      {/* Top Header & Language Selector */}
      <div className="bg-white rounded-2xl border border-ivory-300 p-4 md:p-5 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-forest-900">Healthcare Triage Session</h2>
            <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-sage-100 text-forest-900 border border-sage-200">
              Live Engine
            </span>
          </div>
          <p className="text-xs text-charcoal-700/80 mt-0.5">
            Deterministic clinical dialogue, acute warning sign monitoring, and care navigation.
          </p>
        </div>

        {/* Language selector & reset */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <div className="flex items-center bg-ivory-100 rounded-xl p-1 border border-ivory-300 text-xs">
            <Globe className="w-3.5 h-3.5 text-sage-600 ml-2 mr-1" />
            <button
              type="button"
              onClick={() => setSelectedLanguage('hinglish')}
              className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
                selectedLanguage === 'hinglish'
                  ? 'bg-forest-800 text-ivory-50 shadow-soft'
                  : 'text-charcoal-700 hover:text-forest-900'
              }`}
            >
              Hinglish
            </button>
            <button
              type="button"
              onClick={() => setSelectedLanguage('hi')}
              className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
                selectedLanguage === 'hi'
                  ? 'bg-forest-800 text-ivory-50 shadow-soft'
                  : 'text-charcoal-700 hover:text-forest-900'
              }`}
            >
              हिंदी
            </button>
            <button
              type="button"
              onClick={() => setSelectedLanguage('en')}
              className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
                selectedLanguage === 'en'
                  ? 'bg-forest-800 text-ivory-50 shadow-soft'
                  : 'text-charcoal-700 hover:text-forest-900'
              }`}
            >
              English
            </button>
          </div>

          <button
            type="button"
            onClick={() => initializeSession(selectedLanguage)}
            title="Start New Session"
            className="p-2 rounded-xl border border-ivory-300 bg-white hover:bg-ivory-100 text-charcoal-700 hover:text-forest-900 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Emergency Escalation Alert Card (Prominent if triggered) */}
      {safetyStatus?.is_emergency && (
        <div className="p-5 rounded-2xl border-2 border-red-500 bg-red-50 text-red-950 shadow-card animate-pulse space-y-3">
          <div className="flex items-start gap-3">
            <ShieldAlert className="w-6 h-6 text-red-600 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <h3 className="text-base font-bold text-red-900">
                CRITICAL MEDICAL EMERGENCY DETECTED
              </h3>
              <p className="text-xs text-red-800 leading-relaxed">
                Your reported symptoms indicate an acute red-flag warning sign. Routine online questioning
                has been halted for your safety.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <a
              href="tel:112"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-soft transition-colors"
            >
              <PhoneCall className="w-4 h-4" />
              <span>Dial 112 (National Emergency)</span>
            </a>
            <a
              href="tel:108"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white border border-red-300 text-red-700 hover:bg-red-100 font-semibold text-xs transition-colors"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>Ambulance 108</span>
            </a>
            <span className="text-[11px] text-red-700/80">
              Proceed to the nearest emergency room immediately.
            </span>
          </div>
        </div>
      )}

      {/* Main Dialogue Container */}
      <div className="bg-white rounded-2xl border border-ivory-300 shadow-card flex flex-col overflow-hidden h-[540px]">
        {/* Dialogue Progress Bar */}
        <div className="px-5 py-3 border-b border-ivory-200 bg-ivory-50 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-forest-800" />
            <span className="font-semibold text-forest-900">Clinical Consultation Flow</span>
          </div>

          {currentQuestion && !isComplete && (
            <div className="flex items-center gap-2 text-xs">
              <span className="text-[11px] font-semibold text-forest-900 px-2 py-0.5 rounded-md bg-sage-100 border border-sage-200">
                Question {currentQuestion.question_index} of {currentQuestion.total_questions}
              </span>
              <span className="text-[11px] text-charcoal-700/70 capitalize hidden sm:inline">
                ({currentQuestion.category})
              </span>
            </div>
          )}

          {isComplete && (
            <span className="text-[11px] font-semibold text-emerald-800 px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-emerald-600" />
              Triage Assessment Ready
            </span>
          )}
        </div>

        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {sessionError && (
            <div className="p-3.5 rounded-xl border border-red-200 bg-red-50 text-red-900 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0 text-red-600" />
              <span>{sessionError}</span>
            </div>
          )}

          {messages.map((msg) => {
            const isAsst = msg.role === 'assistant';
            return (
              <div
                key={msg.id}
                className={`flex items-start gap-3 ${isAsst ? 'justify-start' : 'justify-end'}`}
              >
                {isAsst && (
                  <div className="w-8 h-8 rounded-xl bg-forest-800 text-ivory-50 flex items-center justify-center shrink-0 shadow-soft">
                    <Activity className="w-4 h-4 text-sage-200" />
                  </div>
                )}

                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-soft ${
                    isAsst
                      ? 'bg-ivory-100 border border-ivory-300 text-charcoal-900 rounded-tl-sm'
                      : 'bg-forest-800 text-ivory-50 rounded-tr-sm'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  <p
                    className={`text-[9px] mt-1.5 text-right ${
                      isAsst ? 'text-charcoal-700/60' : 'text-ivory-200/70'
                    }`}
                  >
                    {msg.time}
                  </p>
                </div>

                {!isAsst && (
                  <div className="w-8 h-8 rounded-xl bg-sage-200 text-forest-900 flex items-center justify-center shrink-0 font-bold text-xs">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-forest-800 text-ivory-50 flex items-center justify-center shrink-0">
                <Activity className="w-4 h-4 text-sage-200 animate-pulse" />
              </div>
              <div className="bg-ivory-100 border border-ivory-300 rounded-2xl rounded-tl-sm px-4 py-2.5 text-xs text-charcoal-700/80 flex items-center gap-2">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-forest-800" />
                <span>CuraGennie is analyzing symptoms and safety rules...</span>
              </div>
            </div>
          )}

          <div ref={chatBottomRef} />
        </div>

        {/* Input Form or Completed State */}
        <div className="p-4 border-t border-ivory-200 bg-ivory-50 space-y-2">
          {!isComplete && !safetyStatus?.is_emergency ? (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your symptoms or answer follow-up question in English, Hindi, or Hinglish..."
                disabled={loading}
                className="flex-1 px-4 py-2.5 text-xs rounded-xl border border-ivory-300 bg-white text-charcoal-900 placeholder:text-charcoal-700/40 focus:outline-none focus:ring-2 focus:ring-forest-800 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!inputText.trim() || loading}
                className="px-4 py-2.5 rounded-xl bg-forest-800 text-ivory-50 hover:bg-forest-900 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shrink-0 shadow-soft flex items-center gap-1.5 text-xs font-semibold"
              >
                <span>Send</span>
                <Send className="w-3.5 h-3.5" />
              </button>
            </form>
          ) : (
            <div className="flex items-center justify-between text-xs py-1">
              <span className="text-charcoal-700/80 font-medium">
                {safetyStatus?.is_emergency
                  ? 'Emergency protocol active. Please call 112.'
                  : 'Consultation dialogue concluded.'}
              </span>
              <button
                type="button"
                onClick={() => initializeSession(selectedLanguage)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors"
              >
                <RotateCcw className="w-3 h-3" />
                <span>Start Fresh Consultation</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Sample Clinical Prompts for Quick Testing */}
      <div className="space-y-2">
        <p className="text-xs font-semibold text-forest-900 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-sage-600" />
          <span>Quick Test Prompts (Tap to evaluate engine response):</span>
        </p>
        <div className="flex flex-wrap items-center gap-2">
          {samplePrompts.map((prompt) => (
            <button
              key={prompt.label}
              type="button"
              onClick={() => handleSendMessage(prompt.text)}
              disabled={loading || isComplete}
              className="text-[11px] font-medium px-3 py-1.5 rounded-lg border border-ivory-300 bg-white hover:bg-sage-100 hover:border-sage-300 text-charcoal-800 transition-colors disabled:opacity-40 text-left"
            >
              {prompt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Structured Clinical Assessment Card (When available) */}
      {assessment && (
        <div className="bg-white rounded-2xl border border-sage-300 p-6 shadow-card space-y-6">
          <div className="flex items-start justify-between gap-4 border-b border-ivory-200 pb-4">
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-sage-100 text-forest-900 text-[10px] font-bold uppercase tracking-wider mb-1">
                <FileText className="w-3 h-3 text-sage-600" />
                Structured Clinical Summary
              </div>
              <h3 className="text-lg font-bold text-forest-900">
                {assessment.main_concern}
              </h3>
              <p className="text-xs text-charcoal-700/80 mt-0.5">
                Timeline: <strong className="font-semibold text-forest-900">{assessment.duration_timeline}</strong>
              </p>
            </div>

            <div className="shrink-0 text-right">
              <span className="text-[10px] font-bold px-3 py-1 rounded-full border bg-sage-50 text-forest-900 border-sage-300">
                {assessment.is_escalated ? 'EMERGENCY ESCALATED' : 'OUTPATIENT GUIDANCE'}
              </span>
            </div>
          </div>

          {/* Potential Explanations */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-forest-900 uppercase tracking-wider flex items-center gap-1.5">
              <span>Potential Explanations (Non-Diagnostic)</span>
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {assessment.potential_explanations.map((exp, idx) => (
                <div key={idx} className="p-3.5 rounded-xl border border-ivory-300 bg-ivory-50 space-y-1">
                  <p className="text-xs font-bold text-forest-900">{exp.title}</p>
                  <p className="text-xs text-charcoal-700/90 leading-relaxed">{exp.reasoning}</p>
                  <span className="text-[10px] text-sage-600 font-semibold block pt-1">
                    Context: {exp.likelihood_context}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Suggested Next Steps */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-forest-900 uppercase tracking-wider">
              Suggested Care Next Steps
            </h4>
            <ul className="space-y-1.5">
              {assessment.suggested_next_steps.map((step, idx) => (
                <li key={idx} className="text-xs text-charcoal-800 flex items-start gap-2">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Actions: Browse Verified Doctors */}
          <div className="pt-2 flex flex-wrap items-center justify-between gap-3 border-t border-ivory-200">
            <p className="text-[11px] text-charcoal-700/70 italic max-w-xl">
              {assessment.disclaimer}
            </p>

            {onNavigate && (
              <button
                type="button"
                onClick={() => onNavigate('doctors')}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
              >
                <span>Find Recommended Specialists</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
