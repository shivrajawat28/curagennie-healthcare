import { useState, useEffect, useRef, useCallback } from 'react';

export interface UseAudioVisualizerReturn {
  audioEnergy: number; // 0.0 to 1.0 normalized
  frequencyData: Uint8Array;
  startVisualizer: () => Promise<void>;
  stopVisualizer: () => void;
}

export function useAudioVisualizer(): UseAudioVisualizerReturn {
  const [audioEnergy, setAudioEnergy] = useState<number>(0);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const dataArrayRef = useRef<Uint8Array>(new Uint8Array(32));

  const updateVisualizer = useCallback(() => {
    if (!analyserRef.current) return;

    analyserRef.current.getByteFrequencyData(dataArrayRef.current);

    // Compute Root Mean Square (RMS) energy normalized between 0.0 and 1.0
    let sum = 0;
    const len = dataArrayRef.current.length;
    for (let i = 0; i < len; i++) {
      sum += dataArrayRef.current[i] * dataArrayRef.current[i];
    }
    const rms = Math.sqrt(sum / len);
    const normalizedEnergy = Math.min(1.0, rms / 128);

    setAudioEnergy(normalizedEnergy);
    animationFrameRef.current = requestAnimationFrame(updateVisualizer);
  }, []);

  const startVisualizer = useCallback(async () => {
    try {
      if (mediaStreamRef.current) {
        return; // already active
      }

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
      mediaStreamRef.current = stream;

      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      const audioCtx = new AudioContextClass();
      audioContextRef.current = audioCtx;

      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 64;
      analyser.smoothingTimeConstant = 0.8;
      analyserRef.current = analyser;

      dataArrayRef.current = new Uint8Array(analyser.frequencyBinCount);

      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);

      animationFrameRef.current = requestAnimationFrame(updateVisualizer);
    } catch (err) {
      console.warn('Web Audio API visualizer stream access error:', err);
    }
  }, [updateVisualizer]);

  const stopVisualizer = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }

    if (audioContextRef.current) {
      try {
        audioContextRef.current.close();
      } catch {}
      audioContextRef.current = null;
    }

    analyserRef.current = null;
    setAudioEnergy(0);
  }, []);

  useEffect(() => {
    return () => {
      stopVisualizer();
    };
  }, [stopVisualizer]);

  return {
    audioEnergy,
    frequencyData: dataArrayRef.current,
    startVisualizer,
    stopVisualizer,
  };
}
