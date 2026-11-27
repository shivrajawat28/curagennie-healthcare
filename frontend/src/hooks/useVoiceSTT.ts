import { useState, useEffect, useRef, useCallback } from 'react';

export type STTLanguage = 'en-IN' | 'hi-IN' | 'hinglish';

export interface UseVoiceSTTReturn {
  isSupported: boolean;
  isListening: boolean;
  isProcessing: boolean;
  transcript: string;
  interimTranscript: string;
  error: string | null;
  permissionDenied: boolean;
  startListening: (lang?: STTLanguage) => Promise<void>;
  stopListening: () => void;
  resetTranscript: () => void;
  setTranscript: (text: string) => void;
}

// Window declaration for Web Speech API vendor prefixes
interface IWindow extends Window {
  webkitSpeechRecognition?: any;
  SpeechRecognition?: any;
}

export function useVoiceSTT(defaultLanguage: STTLanguage = 'hinglish'): UseVoiceSTTReturn {
  const [isSupported, setIsSupported] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [permissionDenied, setPermissionDenied] = useState(false);

  const recognitionRef = useRef<any>(null);
  const silenceTimerRef = useRef<any>(null);
  const currentLangRef = useRef<STTLanguage>(defaultLanguage);

  useEffect(() => {
    const win = window as unknown as IWindow;
    const SpeechRecognitionClass = win.SpeechRecognition || win.webkitSpeechRecognition;
    if (SpeechRecognitionClass) {
      setIsSupported(true);
    } else {
      setIsSupported(false);
    }
  }, []);

  const getRecognitionLang = (lang: STTLanguage): string => {
    switch (lang) {
      case 'hi-IN':
        return 'hi-IN';
      case 'en-IN':
        return 'en-IN';
      case 'hinglish':
      default:
        // Best browser configuration for Indian English/Hinglish phonetics
        return 'hi-IN';
    }
  };

  const stopListening = useCallback(() => {
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
      silenceTimerRef.current = null;
    }
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // already stopped
      }
    }
    setIsListening(false);
    setIsProcessing(false);
  }, []);

  const startListening = useCallback(
    async (lang?: STTLanguage) => {
      setError(null);
      setPermissionDenied(false);
      setInterimTranscript('');

      const win = window as unknown as IWindow;
      const SpeechRecognitionClass = win.SpeechRecognition || win.webkitSpeechRecognition;

      if (!SpeechRecognitionClass) {
        setError('Browser Web Speech API is not supported in this browser. Please use Chrome/Edge or text input.');
        return;
      }

      if (lang) {
        currentLangRef.current = lang;
      }

      // Check mic permission explicitly before starting
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          // Stop media tracks immediately — recognition manages its own stream
          stream.getTracks().forEach((track) => track.stop());
        }
      } catch (err: any) {
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          setPermissionDenied(true);
          setError('Microphone permission was denied. Please allow microphone access in your browser settings.');
          return;
        }
      }

      try {
        if (recognitionRef.current) {
          try {
            recognitionRef.current.abort();
          } catch {}
        }

        const recognition = new SpeechRecognitionClass();
        recognitionRef.current = recognition;

        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        recognition.lang = getRecognitionLang(currentLangRef.current);

        recognition.onstart = () => {
          setIsListening(true);
          setIsProcessing(false);
        };

        recognition.onresult = (event: any) => {
          let currentInterim = '';
          let currentFinal = '';

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            const piece = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              currentFinal += piece + ' ';
            } else {
              currentInterim += piece;
            }
          }

          if (currentFinal) {
            setTranscript((prev) => (prev ? `${prev.trim()} ${currentFinal.trim()}` : currentFinal.trim()));
          }
          setInterimTranscript(currentInterim);

          // Reset silence timer on speech
          if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);
          silenceTimerRef.current = setTimeout(() => {
            // After 4.5 seconds of silence, stop listening automatically
            stopListening();
          }, 4500);
        };

        recognition.onerror = (event: any) => {
          console.warn('SpeechRecognition error:', event.error);
          if (event.error === 'not-allowed') {
            setPermissionDenied(true);
            setError('Microphone permission was denied.');
          } else if (event.error === 'no-speech') {
            // no-speech is normal during pauses; do not show error banner
          } else {
            setError(`Recognition note: ${event.error}. You can edit text manually.`);
          }
          setIsListening(false);
          setIsProcessing(false);
        };

        recognition.onend = () => {
          setIsListening(false);
          setIsProcessing(false);
          setInterimTranscript('');
        };

        recognition.start();
      } catch (err: any) {
        console.error('Error starting SpeechRecognition:', err);
        setError('Could not start microphone speech recognition.');
        setIsListening(false);
      }
    },
    [stopListening]
  );

  const resetTranscript = useCallback(() => {
    setTranscript('');
    setInterimTranscript('');
    setError(null);
  }, []);

  return {
    isSupported,
    isListening,
    isProcessing,
    transcript,
    interimTranscript,
    error,
    permissionDenied,
    startListening,
    stopListening,
    resetTranscript,
    setTranscript,
  };
}
