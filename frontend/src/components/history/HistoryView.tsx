import React, { useState, useEffect } from 'react';
import { ConsultationDetail, NavRoute } from '../../types';
import { apiService } from '../../services/api';
import {
  Clock,
  Calendar,
  FileText,
  Search,
  CheckCircle,
  ChevronRight,
  X,
  Plus,
  PlayCircle,
  Printer,
} from 'lucide-react';

interface HistoryViewProps {
  onNavigate: (route: NavRoute, sessionId?: string) => void;
}

export const HistoryView: React.FC<HistoryViewProps> = ({ onNavigate }) => {
  const [consultations, setConsultations] = useState<ConsultationDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSession, setSelectedSession] = useState<ConsultationDetail | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const loadConsultations = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getConsultations();
      setConsultations(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load consultation records');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConsultations();
  }, []);

  const filtered = consultations.filter((item) => {
    const matchesRisk = filterRisk === 'all' || item.risk_level.toLowerCase() === filterRisk.toLowerCase();
    const matchesSearch =
      item.chief_complaint.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.language.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesRisk && matchesSearch;
  });

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-forest-900 flex items-center gap-2">
            <Clock className="w-5 h-5 text-sage-600" />
            <span>Consultation History & Summaries</span>
          </h2>
          <p className="text-xs text-charcoal-700/80 mt-1">
            Historical health inquiries, triage assessments, and clinical recommendations.
          </p>
        </div>

        <button
          onClick={() => onNavigate('new-consultation')}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>New Consultation</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-ivory-300 p-3.5 shadow-soft flex flex-col md:flex-row gap-3 items-center justify-between">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-charcoal-700/50 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search symptoms or complaint..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
          />
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <span className="text-xs text-charcoal-700/70 font-medium">Risk Filter:</span>
          {['all', 'low', 'medium', 'high'].map((level) => (
            <button
              key={level}
              onClick={() => setFilterRisk(level)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold capitalize transition-colors ${
                filterRisk === level
                  ? 'bg-forest-800 text-ivory-50'
                  : 'bg-ivory-100 text-charcoal-700 hover:bg-ivory-200'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {/* Consultations List */}
      {loading ? (
        <div className="p-12 text-center text-charcoal-700">
          <Clock className="w-6 h-6 animate-spin mx-auto mb-2 text-forest-800" />
          <p className="text-xs font-medium">Retrieving saved clinical transcripts...</p>
        </div>
      ) : error ? (
        <div className="p-6 rounded-xl border border-red-200 bg-red-50 text-red-900 text-xs text-center space-y-2">
          <p>{error}</p>
          <button
            onClick={loadConsultations}
            className="px-3 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold"
          >
            Retry
          </button>
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-ivory-300 space-y-2">
          <FileText className="w-8 h-8 text-sage-400 mx-auto" />
          <p className="text-sm font-semibold text-forest-900">No consultation records match</p>
          <p className="text-xs text-charcoal-700/70">
            {searchQuery ? 'Try clearing your search query.' : 'Start a consultation to create records.'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {filtered.map((item) => {
            const isMedium = item.risk_level === 'medium';
            const isHigh = item.risk_level === 'high' || item.risk_level === 'emergency';

            return (
              <div
                key={item.id}
                onClick={() => setSelectedSession(item)}
                className="p-5 rounded-xl border border-ivory-300 bg-white hover:border-sage-400/80 transition-all cursor-pointer shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-bold text-forest-900">
                      {item.chief_complaint}
                    </span>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-ivory-100 text-charcoal-700 capitalize">
                      {item.language}
                    </span>
                  </div>

                  <p className="text-xs text-charcoal-700/70 flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5 text-sage-600" />
                    <span>
                      {new Date(item.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                    <span>•</span>
                    <span>{item.messages.length} messages</span>
                  </p>
                </div>

                <div className="flex items-center gap-4 shrink-0">
                  <span
                    className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${
                      isHigh
                        ? 'bg-red-50 text-red-700 border-red-200'
                        : isMedium
                        ? 'bg-amber-50 text-amber-800 border-amber-200'
                        : 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    }`}
                  >
                    {item.risk_level.toUpperCase()} RISK
                  </span>

                  <ChevronRight className="w-4 h-4 text-charcoal-700/40 group-hover:text-forest-900 group-hover:translate-x-0.5 transition-all" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Detail & Clinical Summary Modal */}
      {selectedSession && (
        <div className="fixed inset-0 z-50 bg-forest-950/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full border border-ivory-300 shadow-card max-h-[85vh] flex flex-col overflow-hidden">
            <div className="p-5 border-b border-ivory-200 flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-forest-900">Clinical Consultation Record</h3>
                <p className="text-xs text-charcoal-700/70 font-mono">ID: {selectedSession.id}</p>
              </div>
              <button
                onClick={() => setSelectedSession(null)}
                className="p-1 rounded-lg text-charcoal-700 hover:bg-ivory-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-5 text-xs text-charcoal-800">
              {/* Chief Complaint Banner */}
              <div className="p-3.5 rounded-xl bg-ivory-100 border border-ivory-300 space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-charcoal-700/70">
                  Reported Chief Complaint
                </span>
                <p className="text-sm font-semibold text-forest-900">
                  {selectedSession.chief_complaint}
                </p>
              </div>

              {/* Structured Summary if available */}
              {selectedSession.summary && (
                <div className="p-4 rounded-xl border border-sage-200 bg-sage-50/70 space-y-2.5">
                  <h4 className="text-xs font-bold text-forest-900 uppercase tracking-wider flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5 text-forest-800" />
                    <span>Clinical Triage Assessment</span>
                  </h4>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="font-semibold text-forest-900">Assessment: </span>
                      {selectedSession.summary.chief_complaint}
                    </div>
                    <div>
                      <span className="font-semibold text-forest-900">Duration: </span>
                      {selectedSession.summary.duration}
                    </div>
                    <div className="col-span-2">
                      <span className="font-semibold text-forest-900">Care Plan / Action: </span>
                      {selectedSession.summary.recommended_action}
                    </div>
                  </div>
                </div>
              )}

              {/* Dialogue Transcript */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-forest-900 uppercase tracking-wider">
                  Consultation Transcript ({selectedSession.messages.length} messages)
                </h4>
                {selectedSession.messages.length > 0 ? (
                  <div className="space-y-2">
                    {selectedSession.messages.map((m) => (
                      <div
                        key={m.id}
                        className={`p-3 rounded-lg text-xs leading-relaxed ${
                          m.role === 'assistant'
                            ? 'bg-ivory-100 border border-ivory-300 text-forest-950 ml-0 mr-8'
                            : 'bg-forest-800 text-ivory-50 ml-8 mr-0'
                        }`}
                      >
                        <p className="font-bold text-[10px] mb-1 opacity-80 uppercase tracking-wider">
                          {m.role === 'assistant' ? 'CuraGennie Assistant' : 'Patient'}
                        </p>
                        <p>{m.content}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-charcoal-700/70 italic">Transcript recorded via intake form.</p>
                )}
              </div>
            </div>

            <div className="p-4 border-t border-ivory-200 bg-ivory-50 flex items-center justify-between gap-2 flex-wrap">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => {
                    const id = selectedSession.id;
                    setSelectedSession(null);
                    onNavigate('new-consultation', id);
                  }}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
                >
                  <PlayCircle className="w-3.5 h-3.5" />
                  <span>Resume in Consultation View</span>
                </button>

                <button
                  type="button"
                  onClick={() => window.print()}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-ivory-300 bg-white text-forest-900 text-xs font-semibold hover:bg-ivory-100 transition-colors"
                >
                  <Printer className="w-3.5 h-3.5 text-forest-800" />
                  <span>Print Record</span>
                </button>
              </div>

              <button
                type="button"
                onClick={() => setSelectedSession(null)}
                className="px-4 py-2 rounded-xl border border-ivory-300 bg-white text-charcoal-700 text-xs font-semibold hover:bg-ivory-100"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
