import React, { useState, useEffect, useRef } from 'react';
import {
  NavRoute,
  EngineResponse,
  AssessmentResponse,
  QuestionDetail,
  SafetyStatus,
} from '../../types';
import { apiService } from '../../services/api';
import { useVoiceSTT, STTLanguage } from '../../hooks/useVoiceSTT';
import { useVoiceTTS } from '../../hooks/useVoiceTTS';
import { useAudioVisualizer } from '../../hooks/useAudioVisualizer';
import { AudioWaveform } from '../voice/AudioWaveform';
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
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Radio,
} from 'lucide-react';

interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  time: string;
}

interface NewConsultationViewProps {
  initialSessionId?: string | null;
  onNavigate?: (route: NavRoute) => void;
}

export const NewConsultationView: React.FC<NewConsultationViewProps> = ({
  initialSessionId,
  onNavigate,
}) => {
  const [selectedLanguage, setSelectedLanguage] = useState<'hinglish' | 'hi' | 'en'>('hinglish');
  const [sessionId, setSessionId] = useState<string | null>(initialSessionId || null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionError, setSessionError] = useState<string | null>(null);

  const [currentQuestion, setCurrentQuestion] = useState<QuestionDetail | null>(null);
  const [safetyStatus, setSafetyStatus] = useState<SafetyStatus | null>(null);
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [isComplete, setIsComplete] = useState(false);

  // Auto-play voice state
  const [autoVoiceReply, setAutoVoiceReply] = useState<boolean>(true);

  // Hooks for Voice STT, TTS, and Audio Visualizer
  const sttLanguage: STTLanguage =
    selectedLanguage === 'hi' ? 'hi-IN' : selectedLanguage === 'en' ? 'en-IN' : 'hinglish';
  const voiceSTT = useVoiceSTT(sttLanguage);
  const voiceTTS = useVoiceTTS();
  const audioVisualizer = useAudioVisualizer();

  const chatBottomRef = useRef<HTMLDivElement>(null);

  // Sync STT transcript into input text when available
  useEffect(() => {
    if (voiceSTT.transcript) {
      setInputText(voiceSTT.transcript);
    }
  }, [voiceSTT.transcript]);

  // Load existing session if initialSessionId was provided, otherwise initialize a new one
  useEffect(() => {
    if (initialSessionId) {
      loadExistingSession(initialSessionId);
    } else {
      initializeSession(selectedLanguage);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialSessionId]);

  const loadExistingSession = async (sid: string) => {
    setLoading(true);
    setSessionError(null);
    try {
      const detail = await apiService.getConsultationDetail(sid);
      setSessionId(detail.id);
      if (detail.language === 'hi' || detail.language === 'en' || detail.language === 'hinglish') {
        setSelectedLanguage(detail.language);
      }
      setMessages(
        detail.messages.map((m: any) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          time: new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }))
      );
      if (detail.assessment) {
        setAssessment(detail.assessment);
      }
      setIsComplete(detail.state === 'COMPLETED' || detail.state === 'ESCALATED');
      if (detail.state === 'ESCALATED') {
        setSafetyStatus({
          is_emergency: true,
          is_ambiguous: false,
          red_flags_detected: ['emergency'],
          action_required: 'ESCALATE_EMERGENCY',
          emergency_contact: '112 / 108',
        });
      }
    } catch (err: any) {
      setSessionError(err.message || 'Failed to load existing session.');
    } finally {
      setLoading(false);
    }
  };

  // Initialize a new consultation session
  const initializeSession = async (lang: 'hinglish' | 'hi' | 'en') => {
    setLoading(true);
    setSessionError(null);
    setAssessment(null);
    setIsComplete(false);
    setCurrentQuestion(null);
    setSafetyStatus(null);
    voiceTTS.stop();
    if (voiceSTT.isListening) {
      voiceSTT.stopListening();
      audioVisualizer.stopVisualizer();
    }

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

      if (autoVoiceReply && voiceTTS.isSupported) {
        voiceTTS.speak(res.assistant_message, lang === 'hi' ? 'hi-IN' : 'en-IN');
      }
    } catch (err: any) {
      setSessionError(err.message || 'Failed to initialize consultation session with backend.');
    } finally {
      setLoading(false);
    }
  };

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading, voiceSTT.interimTranscript]);

  // Voice Recording Toggle Handler
  const toggleRecording = async () => {
    if (voiceSTT.isListening) {
      voiceSTT.stopListening();
      audioVisualizer.stopVisualizer();
    } else {
      voiceTTS.stop();
      try {
        await voiceSTT.startListening(sttLanguage);
        await audioVisualizer.startVisualizer();
      } catch (err) {
        console.warn('Voice recording activation error:', err);
      }
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || !sessionId || loading) return;

    // If microphone is running, stop it
    if (voiceSTT.isListening) {
      voiceSTT.stopListening();
      audioVisualizer.stopVisualizer();
    }

    // Add user message to UI immediately
    const userMsg: ChatMessage = {
      id: 'user-' + Date.now(),
      role: 'user',
      content: text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    voiceSTT.resetTranscript();
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

      // Speak reply if auto voice is enabled
      if (autoVoiceReply && voiceTTS.isSupported) {
        const langCode = selectedLanguage === 'hi' ? 'hi-IN' : 'en-IN';
        voiceTTS.speak(res.assistant_message, langCode);
      }
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

  const currentWaveState = voiceSTT.isListening
    ? 'listening'
    : voiceSTT.isProcessing
    ? 'processing'
    : 'idle';

  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto space-y-6">
      {/* Top Header & Language Selector */}
      <div className="bg-white rounded-2xl border border-ivory-300 p-4 md:p-5 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-forest-900">Healthcare Triage Session</h2>
            <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-sage-100 text-forest-900 border border-sage-200">
              Voice-First Engine
            </span>
          </div>
          <p className="text-xs text-charcoal-700/80 mt-0.5">
            Voice-enabled clinical dialogue, acute warning sign monitoring, and care navigation.
          </p>
        </div>

        {/* Language selector & reset */}
        <div className="flex items-center gap-2 self-start sm:self-auto flex-wrap">
          {/* TTS Audio Toggle */}
          <button
            type="button"
            onClick={() => {
              if (voiceTTS.isSpeaking) {
                voiceTTS.stop();
              }
              setAutoVoiceReply(!autoVoiceReply);
            }}
            title={autoVoiceReply ? 'Voice speech synthesis enabled' : 'Voice speech muted'}
            className={`p-2 rounded-xl border transition-colors flex items-center gap-1.5 text-xs font-medium ${
              autoVoiceReply
                ? 'bg-sage-100 border-sage-300 text-forest-900'
                : 'bg-ivory-100 border-ivory-300 text-charcoal-700/60'
            }`}
          >
            {autoVoiceReply ? <Volume2 className="w-4 h-4 text-forest-800" /> : <VolumeX className="w-4 h-4" />}
            <span className="hidden sm:inline">{autoVoiceReply ? 'Audio On' : 'Muted'}</span>
          </button>

          {/* Language Selector */}
          <div className="flex items-center bg-ivory-100 rounded-xl p-1 border border-ivory-300 text-xs">
            <Globe className="w-3.5 h-3.5 text-sage-600 ml-2 mr-1" />
            <button
              type="button"
              onClick={() => {
                setSelectedLanguage('hinglish');
                initializeSession('hinglish');
              }}
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
              onClick={() => {
                setSelectedLanguage('hi');
                initializeSession('hi');
              }}
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
              onClick={() => {
                setSelectedLanguage('en');
                initializeSession('en');
              }}
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

          {voiceSTT.error && (
            <div className="p-3 rounded-xl border border-amber-200 bg-amber-50 text-amber-900 text-xs flex items-center justify-between gap-2">
              <span>{voiceSTT.error}</span>
              <button
                type="button"
                onClick={() => voiceSTT.resetTranscript()}
                className="text-[11px] font-bold text-amber-800 underline"
              >
                Dismiss
              </button>
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
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-soft relative group ${
                    isAsst
                      ? 'bg-ivory-100 border border-ivory-300 text-charcoal-900 rounded-tl-sm'
                      : 'bg-forest-800 text-ivory-50 rounded-tr-sm'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>

                  <div className="flex items-center justify-between mt-2 pt-1 border-t border-black/5">
                    <span
                      className={`text-[9px] ${
                        isAsst ? 'text-charcoal-700/60' : 'text-ivory-200/70'
                      }`}
                    >
                      {msg.time}
                    </span>

                    {/* Speaker replay button on assistant messages */}
                    {isAsst && voiceTTS.isSupported && (
                      <button
                        type="button"
                        onClick={() => {
                          const langCode = selectedLanguage === 'hi' ? 'hi-IN' : 'en-IN';
                          if (voiceTTS.isSpeaking) {
                            voiceTTS.stop();
                          } else {
                            voiceTTS.speak(msg.content, langCode);
                          }
                        }}
                        title="Replay Voice Speech"
                        className="p-1 rounded hover:bg-ivory-200 text-charcoal-700/70 hover:text-forest-900 transition-colors"
                      >
                        <Volume2 className="w-3.5 h-3.5 text-sage-600" />
                      </button>
                    )}
                  </div>
                </div>

                {!isAsst && (
                  <div className="w-8 h-8 rounded-xl bg-sage-200 text-forest-900 flex items-center justify-center shrink-0 font-bold text-xs">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {/* Live Interim Speech Preview Bubble */}
          {voiceSTT.isListening && voiceSTT.interimTranscript && (
            <div className="flex items-start gap-3 justify-end animate-pulse">
              <div className="max-w-[80%] rounded-2xl rounded-tr-sm px-4 py-3 text-xs leading-relaxed bg-forest-800/80 text-ivory-100 border border-forest-700 shadow-soft">
                <div className="flex items-center gap-1.5 text-[10px] text-sage-200 font-semibold mb-1">
                  <Radio className="w-3 h-3 text-red-400 animate-ping" />
                  <span>Listening live...</span>
                </div>
                <p className="italic">{voiceSTT.interimTranscript}</p>
              </div>
              <div className="w-8 h-8 rounded-xl bg-forest-800 text-ivory-50 flex items-center justify-center shrink-0">
                <Mic className="w-4 h-4 text-sage-200" />
              </div>
            </div>
          )}

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

        {/* Live Audio Reactive Waveform Banner (When Mic is Active) */}
        {voiceSTT.isListening && (
          <div className="px-5 py-2 bg-sage-50 border-t border-sage-200 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-forest-900 shrink-0">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping" />
              <span>Microphone Active ({selectedLanguage.toUpperCase()})</span>
            </div>
            <div className="flex-1 max-w-sm">
              <AudioWaveform state={currentWaveState} audioEnergy={audioVisualizer.audioEnergy} />
            </div>
            <button
              type="button"
              onClick={toggleRecording}
              className="text-[11px] font-bold px-3 py-1 rounded-lg bg-forest-800 text-ivory-50 hover:bg-forest-900 transition-colors shrink-0"
            >
              Done Speaking
            </button>
          </div>
        )}

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
              {/* Voice Record Button */}
              <button
                type="button"
                onClick={toggleRecording}
                title={voiceSTT.isListening ? 'Stop Listening' : 'Speak Symptoms'}
                className={`p-2.5 rounded-xl border transition-all flex items-center justify-center shrink-0 shadow-soft ${
                  voiceSTT.isListening
                    ? 'bg-red-500 border-red-600 text-white animate-pulse'
                    : 'bg-white border-ivory-300 text-forest-800 hover:bg-sage-100 hover:border-sage-300'
                }`}
              >
                {voiceSTT.isListening ? (
                  <MicOff className="w-4 h-4 text-white" />
                ) : (
                  <Mic className="w-4 h-4 text-forest-800" />
                )}
              </button>

              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  voiceSTT.isListening
                    ? 'Listening... speak naturally in Hindi, Hinglish, or English'
                    : 'Type symptoms or tap mic to speak in Hindi, Hinglish, or English...'
                }
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
                  ? 'Emergency protocol active. Please call 112 or visit nearest hospital.'
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

          {/* Actions: Find Doctors & Hospitals */}
          <div className="pt-2 flex flex-wrap items-center justify-between gap-3 border-t border-ivory-200">
            <p className="text-[11px] text-charcoal-700/70 italic max-w-lg">
              {assessment.disclaimer}
            </p>

            <div className="flex items-center gap-2">
              {onNavigate && (
                <>
                  <button
                    type="button"
                    onClick={() => onNavigate('doctors')}
                    className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
                  >
                    <span>Find Doctors</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                  <button
                    type="button"
                    onClick={() => onNavigate('hospitals')}
                    className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl border border-ivory-300 bg-ivory-100 text-forest-900 text-xs font-semibold hover:bg-ivory-200 transition-colors"
                  >
                    <span>Hospitals & ICU</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
