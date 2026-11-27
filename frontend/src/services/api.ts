import {
  HealthStatus,
  DashboardData,
  ConsultationDetail,
  DoctorListResponse,
  EngineResponse,
  AssessmentResponse,
  HospitalListResponse,
  AppointmentEnquiryPayload,
  AppointmentEnquiryResult,
} from '../types';

const API_BASE = '/api/v1';

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      const errorMessage = errorBody?.error?.message || `HTTP ${response.status}: ${response.statusText}`;
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (err: any) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const apiService = {
  getHealth: () => fetchJson<HealthStatus>('/health'),

  getDashboard: () => fetchJson<DashboardData>('/dashboard'),

  getConsultations: () => fetchJson<ConsultationDetail[]>('/consultations'),

  startConsultation: (language: string = 'hinglish', chief_complaint?: string) =>
    fetchJson<EngineResponse>('/consultations/start', {
      method: 'POST',
      body: JSON.stringify({ language, chief_complaint }),
    }),

  sendMessage: (sessionId: string, content: string) =>
    fetchJson<EngineResponse>(`/consultations/${sessionId}/message`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    }),

  getConsultationDetail: (sessionId: string) =>
    fetchJson<any>(`/consultations/${sessionId}`),

  getAssessment: (sessionId: string) =>
    fetchJson<AssessmentResponse>(`/consultations/${sessionId}/assessment`),

  completeConsultation: (sessionId: string) =>
    fetchJson<any>(`/consultations/${sessionId}/complete`, {
      method: 'POST',
    }),

  getDoctors: (params?: { city?: string; specialty?: string; teleconsult_only?: boolean }) => {
    const query = new URLSearchParams();
    if (params?.city) query.set('city', params.city);
    if (params?.specialty) query.set('specialty', params.specialty);
    if (params?.teleconsult_only) query.set('teleconsult_only', 'true');
    const queryString = query.toString() ? `?${query.toString()}` : '';
    return fetchJson<DoctorListResponse>(`/doctors${queryString}`);
  },

  getHospitals: (params?: { city?: string; department?: string; emergency_only?: boolean }) => {
    const query = new URLSearchParams();
    if (params?.city) query.set('city', params.city);
    if (params?.department) query.set('department', params.department);
    if (params?.emergency_only) query.set('emergency_only', 'true');
    const queryString = query.toString() ? `?${query.toString()}` : '';
    return fetchJson<HospitalListResponse>(`/hospitals${queryString}`);
  },

  submitAppointmentEnquiry: (payload: AppointmentEnquiryPayload) =>
    fetchJson<AppointmentEnquiryResult>('/hospitals/enquire', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
