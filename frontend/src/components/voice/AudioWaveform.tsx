import React, { useEffect, useRef } from 'react';

export type WaveformState = 'idle' | 'listening' | 'processing';

interface AudioWaveformProps {
  state: WaveformState;
  audioEnergy: number; // 0.0 to 1.0 from AnalyserNode
  className?: string;
}

export const AudioWaveform: React.FC<AudioWaveformProps> = ({
  state,
  audioEnergy,
  className = '',
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const phaseRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      if (state === 'idle') {
        // Calm subtle baseline wave
        ctx.beginPath();
        ctx.strokeStyle = '#D2E2D6'; // sage-200
        ctx.lineWidth = 2;
        ctx.moveTo(0, centerY);
        ctx.lineTo(width, centerY);
        ctx.stroke();
      } else if (state === 'listening') {
        // Genuinely reactive multi-layer wave using live audioEnergy
        phaseRef.current += 0.08 + audioEnergy * 0.15;
        const currentPhase = phaseRef.current;

        // Base amplitude scaled by real microphone energy (RMS)
        // Ensure baseline visibility with dynamic scaling up to 75% height
        const amplitude = Math.max(4, audioEnergy * (height * 0.42));

        // Primary waveform (Deep Forest Green)
        ctx.beginPath();
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = '#1E3A2F'; // forest-800
        for (let x = 0; x < width; x++) {
          const progress = x / width;
          // Apply Gaussian envelope so edges taper smoothly to zero
          const envelope = Math.sin(progress * Math.PI);
          const y =
            centerY +
            Math.sin(progress * 12 + currentPhase) * amplitude * envelope +
            Math.sin(progress * 24 - currentPhase * 0.8) * (amplitude * 0.3) * envelope;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        // Secondary harmonic waveform (Muted Sage)
        ctx.beginPath();
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = '#6B8E7C'; // sage-500
        for (let x = 0; x < width; x++) {
          const progress = x / width;
          const envelope = Math.sin(progress * Math.PI);
          const y =
            centerY +
            Math.cos(progress * 14 - currentPhase * 1.2) * (amplitude * 0.7) * envelope;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      } else if (state === 'processing') {
        // Subtle processing animation
        phaseRef.current += 0.05;
        const currentPhase = phaseRef.current;
        const amplitude = 6;

        ctx.beginPath();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#8BAF99'; // sage-400
        for (let x = 0; x < width; x++) {
          const progress = x / width;
          const envelope = Math.sin(progress * Math.PI);
          const y = centerY + Math.sin(progress * 10 + currentPhase) * amplitude * envelope;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [state, audioEnergy]);

  return (
    <div className={`relative flex items-center justify-center ${className}`}>
      <canvas
        ref={canvasRef}
        width={320}
        height={60}
        className="w-full max-w-[320px] h-[60px]"
      />
    </div>
  );
};
