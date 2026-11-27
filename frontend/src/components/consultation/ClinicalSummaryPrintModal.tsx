import React from 'react';
import { AssessmentResponse } from '../../types';
import { Printer, X, Activity, ShieldCheck, CheckCircle } from 'lucide-react';

interface ClinicalSummaryPrintModalProps {
  isOpen: boolean;
  onClose: () => void;
  assessment: AssessmentResponse;
  sessionId?: string | null;
  language?: string;
  chiefComplaint?: string;
}

export const ClinicalSummaryPrintModal: React.FC<ClinicalSummaryPrintModalProps> = ({
  isOpen,
  onClose,
  assessment,
  sessionId,
  language = 'Hinglish / English',
  chiefComplaint,
}) => {
  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  const formattedDate = new Date().toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/60 backdrop-blur-sm">
      <div className="bg-white rounded-2xl border border-ivory-300 max-w-2xl w-full p-6 md:p-8 shadow-card space-y-6 max-h-[92vh] overflow-y-auto print:max-h-none print:overflow-visible print:border-none print:shadow-none print:p-0">
        {/* Modal Controls (Hidden in Print) */}
        <div className="flex items-center justify-between pb-3 border-b border-ivory-200 print:hidden">
          <div className="flex items-center gap-2 text-xs font-semibold text-forest-900">
            <Activity className="w-4 h-4 text-forest-800" />
            <span>Pre-Consultation Clinical Handover Sheet</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print / Save as PDF</span>
            </button>
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-lg text-charcoal-700 hover:bg-ivory-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Document Content */}
        <div className="space-y-6 text-charcoal-900">
          {/* Header */}
          <div className="border-b-2 border-forest-900 pb-4 flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-forest-800 text-ivory-50 flex items-center justify-center text-xs font-bold print:border print:border-black">
                  CG
                </div>
                <h1 className="text-xl font-bold text-forest-900 tracking-tight">CuraGennie Healthcare</h1>
              </div>
              <p className="text-xs text-charcoal-700 mt-1">
                Patient Pre-Consultation Summary & Triage Handover
              </p>
            </div>

            <div className="text-right text-xs space-y-0.5">
              <p className="font-semibold text-forest-900">Generated: {formattedDate}</p>
              {sessionId && <p className="text-[11px] font-mono text-charcoal-700">Ref ID: {sessionId}</p>}
              <p className="text-[11px] text-charcoal-700">Language: {language}</p>
            </div>
          </div>

          {/* Chief Complaint & Status Banner */}
          <div className="p-4 rounded-xl bg-ivory-100 border border-ivory-300 space-y-2">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-charcoal-700">
                Primary Health Concern
              </span>
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${
                  assessment.is_escalated
                    ? 'bg-red-100 text-red-900 border-red-300'
                    : 'bg-sage-100 text-forest-900 border-sage-300'
                }`}
              >
                {assessment.is_escalated ? 'EMERGENCY ESCALATED' : 'OUTPATIENT GUIDANCE'}
              </span>
            </div>
            <p className="text-base font-bold text-forest-900">
              {chiefComplaint || assessment.main_concern}
            </p>
            {assessment.duration_timeline && (
              <p className="text-xs text-charcoal-700">
                Timeline: <strong>{assessment.duration_timeline}</strong>
              </p>
            )}
          </div>

          {/* Patient Reported Observations */}
          <div className="space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-forest-900 border-b border-ivory-200 pb-1 flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-forest-800" />
              <span>Reported Symptoms & Patient Responses</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-lg border border-ivory-200 bg-ivory-50/60">
                <p className="font-semibold text-forest-900 mb-1">Identified Symptoms:</p>
                <div className="flex flex-wrap gap-1">
                  {assessment.reported_symptoms.map((s, idx) => (
                    <span key={idx} className="px-2 py-0.5 rounded bg-white border border-ivory-300 text-[11px]">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-3 rounded-lg border border-ivory-200 bg-ivory-50/60">
                <p className="font-semibold text-forest-900 mb-1">Warning Signs Screened:</p>
                <div className="flex flex-wrap gap-1">
                  {assessment.warning_signs_screened.map((w, idx) => (
                    <span key={idx} className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-900 border border-emerald-200 text-[11px]">
                      ✓ {w}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Follow-up question answers dictionary */}
            {Object.keys(assessment.follow_up_summary).length > 0 && (
              <div className="p-3 rounded-lg border border-ivory-200 bg-ivory-50/60 space-y-1.5 text-xs">
                <p className="font-semibold text-forest-900">Intake Question Details:</p>
                <div className="space-y-1">
                  {Object.entries(assessment.follow_up_summary).map(([q, ans], idx) => (
                    <div key={idx} className="flex flex-col sm:flex-row sm:items-baseline gap-1 text-[11px]">
                      <span className="font-medium text-charcoal-700 capitalize">{q}:</span>
                      <span className="text-forest-900">{ans}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Potential Considerations (Non-Diagnostic) */}
          <div className="space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-forest-900 border-b border-ivory-200 pb-1">
              Differential Considerations for Clinician Review
            </h2>
            <div className="space-y-2">
              {assessment.potential_explanations.map((exp, idx) => (
                <div key={idx} className="p-3 rounded-lg border border-ivory-300 bg-ivory-50 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-forest-900">{exp.title}</span>
                    <span className="text-[10px] text-sage-600 font-semibold">{exp.likelihood_context}</span>
                  </div>
                  <p className="text-charcoal-700 leading-relaxed text-[11px]">{exp.reasoning}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Suggested Next Steps */}
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-forest-900 border-b border-ivory-200 pb-1">
              Suggested Care Navigation
            </h2>
            <ul className="space-y-1 text-xs">
              {assessment.suggested_next_steps.map((step, idx) => (
                <li key={idx} className="flex items-start gap-2 text-[11px]">
                  <span className="text-forest-800 font-bold">•</span>
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Mandatory Clinical Disclaimer */}
          <div className="p-3 rounded-lg border border-ivory-300 bg-ivory-100 text-[10px] text-charcoal-700 space-y-1 leading-relaxed">
            <div className="flex items-center gap-1 font-bold text-forest-900">
              <ShieldCheck className="w-3.5 h-3.5 text-sage-600" />
              <span>Clinical Disclaimer & Notice to Healthcare Providers:</span>
            </div>
            <p>
              This document is an automated, non-diagnostic pre-consultation summary generated by CuraGennie from patient-reported symptoms. It does not establish a definitive medical diagnosis, prescribe pharmaceutical medications, or replace comprehensive clinical evaluation by a qualified medical practitioner.
            </p>
          </div>
        </div>

        {/* Modal Footer Controls (Hidden in Print) */}
        <div className="pt-3 border-t border-ivory-200 flex items-center justify-end gap-2 print:hidden">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl border border-ivory-300 bg-white text-charcoal-700 text-xs font-semibold hover:bg-ivory-100"
          >
            Close
          </button>
          <button
            type="button"
            onClick={handlePrint}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print / Save as PDF</span>
          </button>
        </div>
      </div>
    </div>
  );
};
