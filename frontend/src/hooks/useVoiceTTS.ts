import { useState, useEffect, useRef, useCallback } from 'react';

export interface UseVoiceTTSReturn {
  isSupported: boolean;
  isSpeaking: boolean;
  speak: (text: string, language?: string) => void;
  stop: () => void;
  replay: () => void;
}

export function useVoiceTTS(): UseVoiceTTSReturn {
  const [isSupported, setIsSupported] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const lastSpokenTextRef = useRef<string>('');
  const lastLanguageRef = useRef<string>('en-IN');
  const availableVoicesRef = useRef<SpeechSynthesisVoice[]>([]);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setIsSupported(true);

      const updateVoices = () => {
        availableVoicesRef.current = window.speechSynthesis.getVoices();
      };

      updateVoices();
      window.speechSynthesis.onvoiceschanged = updateVoices;
    }
  }, []);

  const stop = useCallback(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  const findBestVoice = (lang: string): SpeechSynthesisVoice | null => {
    const voices = availableVoicesRef.current;
    if (!voices || voices.length === 0) return null;

    if (lang.startsWith('hi')) {
      const hindiVoice = voices.find((v) => v.lang === 'hi-IN' || v.lang.startsWith('hi'));
      if (hindiVoice) return hindiVoice;
    }

    // Default to Indian English or British/General English
    const indianEngVoice = voices.find((v) => v.lang === 'en-IN');
    if (indianEngVoice) return indianEngVoice;

    const anyEnglish = voices.find((v) => v.lang.startsWith('en'));
    return anyEnglish || voices[0] || null;
  };

  const sanitizeTextForSpeech = (text: string): string => {
    // Strip markdown symbols, emoji alerts, and overly long disclaimers for natural voice output
    let clean = text
      .replace(/⚠️/g, 'Warning:')
      .replace(/[*_#`~[\]]/g, '')
      .replace(/\(112\)/g, '1 1 2')
      .replace(/\(108\)/g, '1 0 8')
      .trim();

    // If text is extremely long (like full multi-paragraph assessment), speak the initial clinical highlights
    if (clean.length > 320) {
      const sentences = clean.split(/[।.\n]/);
      clean = sentences.slice(0, 3).join('. ') + '. Please review your complete assessment summary below.';
    }

    return clean;
  };

  const speak = useCallback(
    (text: string, language: string = 'en-IN') => {
      if (!text || typeof window === 'undefined' || !('speechSynthesis' in window)) return;

      // Stop any existing speech to prevent overlapping
      window.speechSynthesis.cancel();

      const textToSpeak = sanitizeTextForSpeech(text);
      lastSpokenTextRef.current = text;
      lastLanguageRef.current = language;

      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      const voice = findBestVoice(language);
      if (voice) {
        utterance.voice = voice;
      }
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      utterance.onstart = () => {
        setIsSpeaking(true);
      };

      utterance.onend = () => {
        setIsSpeaking(false);
      };

      utterance.onerror = (e) => {
        console.warn('SpeechSynthesis error:', e);
        setIsSpeaking(false);
      };

      window.speechSynthesis.speak(utterance);
    },
    []
  );

  const replay = useCallback(() => {
    if (lastSpokenTextRef.current) {
      speak(lastSpokenTextRef.current, lastLanguageRef.current);
    }
  }, [speak]);

  return {
    isSupported,
    isSpeaking,
    speak,
    stop,
    replay,
  };
}
