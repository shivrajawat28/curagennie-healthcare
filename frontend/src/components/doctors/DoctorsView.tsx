import React, { useState, useEffect } from 'react';
import { Doctor, NavRoute } from '../../types';
import { apiService } from '../../services/api';
import {
  UserCheck,
  Search,
  MapPin,
  Video,
  Star,
  RefreshCw,
  Building,
  CheckCircle,
} from 'lucide-react';

interface DoctorsViewProps {
  onNavigate: (route: NavRoute) => void;
}

export const DoctorsView: React.FC<DoctorsViewProps> = ({ onNavigate }) => {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  const [specialties, setSpecialties] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedCity, setSelectedCity] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('');
  const [teleconsultOnly, setTeleconsultOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const loadDoctors = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getDoctors({
        city: selectedCity || undefined,
        specialty: selectedSpecialty || undefined,
        teleconsult_only: teleconsultOnly,
      });
      setDoctors(data.doctors);
      setCities(data.cities);
      setSpecialties(data.specialties);
    } catch (err: any) {
      setError(err.message || 'Failed to load doctors');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, [selectedCity, selectedSpecialty, teleconsultOnly]);

  const filteredDoctors = doctors.filter((doc) => {
    if (!searchQuery) return true;
    return (
      doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.specialty.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.hospital_or_clinic.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <div className="p-6 md:p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-forest-900 flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-sage-600" />
            <span>Find Doctors & Specialists</span>
          </h2>
          <p className="text-xs text-charcoal-700/80 mt-1">
            Book in-person appointments or instant teleconsultation across Indian medical networks.
          </p>
        </div>

        <button
          onClick={() => onNavigate('new-consultation')}
          className="text-xs font-semibold px-4 py-2 rounded-xl bg-sage-100 text-forest-900 hover:bg-sage-200 transition-colors self-start sm:self-auto"
        >
          Check Symptoms First →
        </button>
      </div>

      {/* Filters Bar */}
      <div className="bg-white rounded-xl border border-ivory-300 p-4 shadow-soft space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-charcoal-700/50 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search doctor or clinic..."
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
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800 text-charcoal-800"
            >
              <option value="">All Indian Cities</option>
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Specialty select */}
          <div>
            <select
              value={selectedSpecialty}
              onChange={(e) => setSelectedSpecialty(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-ivory-300 bg-ivory-50 focus:outline-none focus:ring-1 focus:ring-forest-800 text-charcoal-800"
            >
              <option value="">All Specialties</option>
              {specialties.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          {/* Teleconsult checkbox */}
          <label className="flex items-center gap-2 text-xs font-semibold text-forest-900 cursor-pointer select-none px-2 py-1 bg-ivory-50 rounded-lg border border-ivory-300">
            <input
              type="checkbox"
              checked={teleconsultOnly}
              onChange={(e) => setTeleconsultOnly(e.target.checked)}
              className="rounded text-forest-800 focus:ring-forest-800"
            />
            <Video className="w-3.5 h-3.5 text-sage-600" />
            <span>Teleconsult Only</span>
          </label>
        </div>
      </div>

      {/* Doctor Cards Grid */}
      {loading ? (
        <div className="p-12 text-center text-charcoal-700 space-y-2">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto text-forest-800" />
          <p className="text-xs font-medium">Finding available clinicians...</p>
        </div>
      ) : error ? (
        <div className="p-6 rounded-xl border border-red-200 bg-red-50 text-red-900 text-xs text-center space-y-2">
          <p>{error}</p>
          <button
            onClick={loadDoctors}
            className="px-3 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold"
          >
            Retry
          </button>
        </div>
      ) : filteredDoctors.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-ivory-300 space-y-2">
          <UserCheck className="w-8 h-8 text-sage-400 mx-auto" />
          <p className="text-sm font-semibold text-forest-900">No doctors match your criteria</p>
          <p className="text-xs text-charcoal-700/70">Try clearing filters or changing city.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDoctors.map((doc) => (
            <div
              key={doc.id}
              className="bg-white rounded-xl border border-ivory-300 p-5 shadow-soft hover:shadow-card transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-forest-900">{doc.name}</h3>
                    <p className="text-xs font-medium text-sage-600">{doc.specialty}</p>
                  </div>
                  <div className="flex items-center gap-1 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded text-[11px] font-bold text-amber-800">
                    <Star className="w-3 h-3 fill-amber-500 text-amber-500" />
                    <span>{doc.rating}</span>
                  </div>
                </div>

                <p className="text-[11px] text-charcoal-700/70 leading-snug">
                  {doc.qualification} • {doc.experience_years} years experience
                </p>

                <div className="space-y-1 text-xs text-charcoal-700 pt-1">
                  <div className="flex items-center gap-1.5">
                    <Building className="w-3.5 h-3.5 text-sage-500 shrink-0" />
                    <span className="truncate">{doc.hospital_or_clinic}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-sage-500 shrink-0" />
                    <span>{doc.city}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2 pt-1 flex-wrap">
                  {doc.teleconsult_available && (
                    <span className="inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded bg-sage-50 text-forest-900 border border-sage-200">
                      <Video className="w-2.5 h-2.5 text-sage-600" />
                      <span>Teleconsult</span>
                    </span>
                  )}
                  <span className="inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded bg-ivory-100 text-charcoal-700">
                    <CheckCircle className="w-2.5 h-2.5 text-emerald-600" />
                    <span>Verified</span>
                  </span>
                </div>
              </div>

              <div className="pt-3 border-t border-ivory-200 flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-charcoal-700/70 block">Consultation Fee</span>
                  <span className="text-sm font-bold text-forest-900">₹{doc.fee_inr}</span>
                </div>

                <button
                  onClick={() =>
                    alert(
                      `Demo Booking:\n\nConnecting to Dr. ${doc.name} (${doc.specialty}).\nIn Phase 04, direct appointment scheduling and clinical summary sharing will be enabled.`
                    )
                  }
                  className="px-3.5 py-1.5 rounded-lg bg-forest-800 text-ivory-50 text-xs font-semibold hover:bg-forest-900 transition-colors shadow-soft"
                >
                  Book Consult
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
