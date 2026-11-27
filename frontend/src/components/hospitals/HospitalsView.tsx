import React, { useState, useEffect } from 'react';
import { Hospital, NavRoute, AppointmentEnquiryResult } from '../../types';
import { apiService } from '../../services/api';
import {
  Building2,
  Search,
  MapPin,
  PhoneCall,
  ShieldAlert,
  Star,
  RefreshCw,
  CheckCircle,
  X,
  AlertCircle,
  Activity,
} from 'lucide-react';

interface HospitalsViewProps {
  onNavigate: (route: NavRoute) => void;
}

export const HospitalsView: React.FC<HospitalsViewProps> = ({ onNavigate }) => {
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  const [departments, setDepartments] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedCity, setSelectedCity] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [emergencyOnly, setEmergencyOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Appointment Enquiry Modal State
  const [selectedHospital, setSelectedHospital] = useState<Hospital | null>(null);
  const [patientName, setPatientName] = useState('');
  const [contactPhone, setContactPhone] = useState('');
  const [preferredMode, setPreferredMode] = useState<'in-person' | 'teleconsult'>('in-person');
  const [notes, setNotes] = useState('');
  const [enquirySubmitting, setEnquirySubmitting] = useState(false);
  const [enquiryError, setEnquiryError] = useState<string | null>(null);
  const [enquiryResult, setEnquiryResult] = useState<AppointmentEnquiryResult | null>(null);

  const loadHospitals = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getHospitals({
        city: selectedCity || undefined,
        department: selectedDepartment || undefined,
        emergency_only: emergencyOnly,
      });
      setHospitals(data.hospitals);
      setCities(data.cities);
      setDepartments(data.departments);
    } catch (err: any) {
      setError(err.message || 'Failed to load hospital network directory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHospitals();
  }, [selectedCity, selectedDepartment, emergencyOnly]);

  const filteredHospitals = hospitals.filter((hosp) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      hosp.name.toLowerCase().includes(q) ||
      hosp.city.toLowerCase().includes(q) ||
      hosp.departments.some((d) => d.toLowerCase().includes(q))
    );
  });

  const handleOpenEnquiry = (hospital: Hospital) => {
    setSelectedHospital(hospital);
    setEnquiryResult(null);
    setEnquiryError(null);
    setPatientName('');
    setContactPhone('');
    setNotes('');
  };

  const handleSubmitEnquiry = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedHospital || !patientName.trim() || !contactPhone.trim()) {
      setEnquiryError('Please provide patient name and contact phone number.');
      return;
    }

    setEnquirySubmitting(true);
    setEnquiryError(null);
    try {
      const result = await apiService.submitAppointmentEnquiry({
        hospital_id: selectedHospital.id,
        patient_name: patientName.trim(),
        contact_phone: contactPhone.trim(),
        preferred_mode: preferredMode,
        notes: notes.trim() || undefined,
      });
      setEnquiryResult(result);
    } catch (err: any) {
      setEnquiryError(err.message || 'Failed to submit appointment enquiry.');
    } finally {
      setEnquirySubmitting(false);
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-forest-900 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-sage-600" />
            <span>Hospital Network & Emergency Facilities</span>
          </h2>
          <p className="text-xs text-charcoal-700/80 mt-1">
            Verified tertiary hospitals, 24x7 trauma centers, ICU facilities, and clinical departments across India.
          </p>
        </div>

        <button
          onClick={() => onNavigate('new-consultation')}
          className="text-xs font-semibold px-4 py-2 rounded-xl bg-sage-100 text-forest-900 hover:bg-sage-200 transition-colors self-start sm:self-auto"
        >
          Check Symptoms First →
        </button>
      </div>

      {/* Emergency Notice Banner */}
      <div className="p-4 rounded-xl border border-red-300 bg-red-50 text-red-950 text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-soft">
        <div className="flex items-center gap-2.5">
          <ShieldAlert className="w-5 h-5 text-red-600 shrink-0" />
          <div>
            <span className="font-bold">Life-Threatening Emergency?</span>
            <p className="text-[11px] text-red-800">
              Immediate national emergency helpline is <strong>112</strong> or call ambulance at <strong>108</strong>.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <a
            href="tel:112"
            className="px-3 py-1.5 rounded-lg bg-red-600 text-white font-bold text-xs hover:bg-red-700 transition-colors flex items-center gap-1.5"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Call 112</span>
          </a>
          <a
            href="tel:108"
            className="px-3 py-1.5 rounded-lg bg-white border border-red-300 text-red-700 font-semibold text-xs hover:bg-red-100 transition-colors flex items-center gap-1.5"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Call 108</span>
          </a>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="bg-white rounded-xl border border-ivory-300 p-4 shadow-soft space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-charcoal-700/50 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search hospital or department..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
            />
          </div>

          {/* City select */}
          <div>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
            >
              <option value="">All Cities</option>
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Department select */}
          <div>
            <select
              value={selectedDepartment}
              onChange={(e) => setSelectedDepartment(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
            >
              <option value="">All Departments</option>
              {departments.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>

          {/* 24x7 Emergency toggle */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-ivory-300 bg-ivory-50">
            <input
              type="checkbox"
              id="emergency_filter"
              checked={emergencyOnly}
              onChange={(e) => setEmergencyOnly(e.target.checked)}
              className="rounded text-forest-800 focus:ring-forest-800 w-4 h-4"
            />
            <label htmlFor="emergency_filter" className="text-xs text-charcoal-800 font-medium cursor-pointer">
              24x7 Emergency Only
            </label>
          </div>
        </div>
      </div>

      {/* Hospital Cards Grid */}
      {loading ? (
        <div className="bg-white rounded-xl border border-ivory-300 p-12 text-center shadow-soft">
          <RefreshCw className="w-6 h-6 animate-spin text-sage-600 mx-auto mb-2" />
          <p className="text-xs text-charcoal-700/70">Loading hospital facilities and departments...</p>
        </div>
      ) : error ? (
        <div className="bg-red-50 rounded-xl border border-red-200 p-6 text-center text-xs text-red-800 space-y-2">
          <p className="font-semibold">{error}</p>
          <button
            onClick={loadHospitals}
            className="px-3 py-1.5 rounded-lg bg-red-600 text-white font-medium text-xs hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      ) : filteredHospitals.length === 0 ? (
        <div className="bg-white rounded-xl border border-ivory-300 p-12 text-center shadow-soft space-y-2">
          <p className="text-sm font-semibold text-forest-900">No hospitals matched your filters</p>
          <p className="text-xs text-charcoal-700/70">Try resetting filters or expanding search terms.</p>
          <button
            onClick={() => {
              setSelectedCity('');
              setSelectedDepartment('');
              setEmergencyOnly(false);
              setSearchQuery('');
            }}
            className="px-3 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-medium hover:bg-forest-900"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredHospitals.map((hospital) => (
            <div
              key={hospital.id}
              className="bg-white rounded-2xl border border-ivory-300 p-5 shadow-soft hover:shadow-card transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2.5">
                {/* Title & Badge */}
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-bold text-forest-900 leading-snug">{hospital.name}</h3>
                    <p className="text-[11px] text-sage-600 font-medium mt-0.5">{hospital.hospital_type}</p>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-sage-50 text-forest-900 border border-sage-200">
                      {hospital.accreditation}
                    </span>
                    <span className="text-xs font-bold text-charcoal-800 flex items-center gap-0.5 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                      <Star className="w-3 h-3 text-amber-500 fill-amber-500" />
                      {hospital.rating}
                    </span>
                  </div>
                </div>

                {/* Location */}
                <div className="flex items-start gap-1.5 text-xs text-charcoal-700/80">
                  <MapPin className="w-3.5 h-3.5 text-sage-600 shrink-0 mt-0.5" />
                  <span>
                    {hospital.address}, <strong>{hospital.city}</strong>
                  </span>
                </div>

                {/* Facilities Badges */}
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  {hospital.emergency_24x7 && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-900 border border-red-200 flex items-center gap-1">
                      <ShieldAlert className="w-3 h-3 text-red-600" />
                      24x7 Emergency
                    </span>
                  )}
                  {hospital.icu_available && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-200 flex items-center gap-1">
                      <Activity className="w-3 h-3 text-emerald-600" />
                      ICU Available
                    </span>
                  )}
                </div>

                {/* Departments */}
                <div className="space-y-1">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-charcoal-700/60">
                    Clinical Departments:
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {hospital.departments.map((dept) => (
                      <span
                        key={dept}
                        className="text-[10px] px-2 py-0.5 rounded bg-ivory-100 text-charcoal-800 border border-ivory-200 font-medium"
                      >
                        {dept}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="pt-3 border-t border-ivory-200 flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <a
                    href={`tel:${hospital.helpline}`}
                    className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1.5 rounded-lg border border-ivory-300 text-forest-900 hover:bg-ivory-100 transition-colors"
                    title="Direct Hospital Helpline"
                  >
                    <PhoneCall className="w-3 h-3 text-forest-800" />
                    <span>{hospital.helpline}</span>
                  </a>
                  {hospital.ambulance_phone && (
                    <a
                      href={`tel:${hospital.ambulance_phone}`}
                      className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1.5 rounded-lg bg-red-50 border border-red-200 text-red-800 hover:bg-red-100 transition-colors"
                      title="Direct Ambulance Line"
                    >
                      <PhoneCall className="w-3 h-3 text-red-600" />
                      <span>Amb: {hospital.ambulance_phone}</span>
                    </a>
                  )}
                </div>

                <button
                  type="button"
                  onClick={() => handleOpenEnquiry(hospital)}
                  className="px-3.5 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
                >
                  Enquire / Book
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Appointment Enquiry Modal */}
      {selectedHospital && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-2xl border border-ivory-300 max-w-md w-full p-6 shadow-card space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between gap-3 border-b border-ivory-200 pb-3">
              <div>
                <h3 className="text-base font-bold text-forest-900">Hospital Consultation Enquiry</h3>
                <p className="text-xs text-sage-600 font-medium">{selectedHospital.name}</p>
              </div>
              <button
                onClick={() => setSelectedHospital(null)}
                className="p-1 rounded-lg text-charcoal-700 hover:bg-ivory-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {enquiryResult ? (
              <div className="space-y-4 py-2">
                <div className="p-4 rounded-xl border border-emerald-300 bg-emerald-50 text-emerald-950 space-y-2">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                    <h4 className="text-sm font-bold">{enquiryResult.message}</h4>
                  </div>
                  <p className="text-xs leading-relaxed">
                    Provider: <strong>{enquiryResult.provider_name}</strong>
                  </p>
                  <p className="text-[11px] text-emerald-800 font-mono">
                    Reference Enquiry ID: {enquiryResult.enquiry_id}
                  </p>
                </div>

                <div className="p-3.5 rounded-xl border border-ivory-300 bg-ivory-50 text-[11px] text-charcoal-700 space-y-1">
                  <p className="font-semibold text-forest-900">Notice:</p>
                  <p>{enquiryResult.notice}</p>
                </div>

                <button
                  type="button"
                  onClick={() => setSelectedHospital(null)}
                  className="w-full py-2.5 rounded-xl bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors"
                >
                  Done
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmitEnquiry} className="space-y-4 text-xs">
                {enquiryError && (
                  <div className="p-3 rounded-lg border border-red-200 bg-red-50 text-red-900 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
                    <span>{enquiryError}</span>
                  </div>
                )}

                <div className="space-y-1">
                  <label className="font-semibold text-forest-900 block">Patient Full Name *</label>
                  <input
                    type="text"
                    required
                    value={patientName}
                    onChange={(e) => setPatientName(e.target.value)}
                    placeholder="e.g. Ramesh Kumar"
                    className="w-full px-3 py-2 rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
                  />
                </div>

                <div className="space-y-1">
                  <label className="font-semibold text-forest-900 block">Contact Phone Number (India) *</label>
                  <input
                    type="tel"
                    required
                    value={contactPhone}
                    onChange={(e) => setContactPhone(e.target.value)}
                    placeholder="e.g. +91 98765 43210"
                    className="w-full px-3 py-2 rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
                  />
                </div>

                <div className="space-y-1">
                  <label className="font-semibold text-forest-900 block">Preferred Mode</label>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => setPreferredMode('in-person')}
                      className={`py-2 px-3 rounded-lg font-medium border text-center transition-colors ${
                        preferredMode === 'in-person'
                          ? 'bg-forest-800 text-ivory-50 border-forest-800'
                          : 'bg-ivory-50 border-ivory-300 text-charcoal-700'
                      }`}
                    >
                      In-Person Visit
                    </button>
                    <button
                      type="button"
                      onClick={() => setPreferredMode('teleconsult')}
                      className={`py-2 px-3 rounded-lg font-medium border text-center transition-colors ${
                        preferredMode === 'teleconsult'
                          ? 'bg-forest-800 text-ivory-50 border-forest-800'
                          : 'bg-ivory-50 border-ivory-300 text-charcoal-700'
                      }`}
                    >
                      Teleconsultation
                    </button>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="font-semibold text-forest-900 block">Brief Health Concern / Department</label>
                  <textarea
                    rows={2}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Optional: Mention symptoms, prior prescriptions, or department requested..."
                    className="w-full px-3 py-2 rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800"
                  />
                </div>

                <p className="text-[11px] text-charcoal-700/70 italic">
                  * CuraGennie coordinates this enquiry directly with {selectedHospital.name} admission desk.
                </p>

                <div className="pt-2 flex items-center justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setSelectedHospital(null)}
                    disabled={enquirySubmitting}
                    className="px-4 py-2 rounded-lg border border-ivory-300 text-charcoal-700 hover:bg-ivory-100 font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={enquirySubmitting}
                    className="px-4 py-2 rounded-lg bg-forest-800 text-ivory-50 font-semibold hover:bg-forest-900 transition-colors shadow-soft flex items-center gap-1.5"
                  >
                    {enquirySubmitting ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Submitting...</span>
                      </>
                    ) : (
                      <span>Submit Appointment Enquiry</span>
                    )}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
