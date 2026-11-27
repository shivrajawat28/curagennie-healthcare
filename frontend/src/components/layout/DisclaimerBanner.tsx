import React from 'react';
import { AlertCircle, PhoneCall } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  return (
    <div className="bg-sage-100/70 border-b border-sage-200/80 px-6 py-2.5 text-xs text-charcoal-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
      <div className="flex items-center gap-2">
        <AlertCircle className="w-4 h-4 text-forest-800 shrink-0" />
        <p className="leading-snug">
          <strong className="font-semibold text-forest-900">Medical Navigation Notice:</strong>{' '}
          CuraGennie provides health navigation, symptom triage, and education. It is not an autonomous diagnostic or prescription system.
        </p>
      </div>

      <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto text-[11px] font-medium text-warmred-600 bg-white/80 px-2.5 py-1 rounded-md border border-red-100">
        <PhoneCall className="w-3 h-3 text-warmred-600 shrink-0" />
        <span>India Emergency: Call 112 / 108</span>
      </div>
    </div>
  );
};
