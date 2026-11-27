export type NavRoute = 'dashboard' | 'new-consultation' | 'history' | 'doctors' | 'settings';

export type LanguageCode = 'en' | 'hi' | 'hinglish';

export interface HealthStatus {
  status: string;
  app_name: string;
  version: string;
  environment: string;
  database_connected: boolean;
  ai_provider_configured: boolean;
  mode: string;
  details: {
    zero_key_mode: boolean;
    voice_stt_mode: string;
    voice_tts_mode: string;
    database_driver: string;
    supported_languages: string[];
  };
}

export interface RecentConsultationSummary {
  id: string;
  created_at: string;
  chief_complaint: string;
  language: string;
  risk_level: 'low' | 'medium' | 'high' | 'emergency';
  stage: string;
  status: string;
}

export interface GuidanceTip {
  id: string;
  title: string;
  summary: string;
  tag: string;
  action_text?: string;
}

export interface DashboardData {
  welcome_message: string;
  user_name: string;
  stats: {
    total_consultations: number;
    completed_consultations: number;
    verified_doctors_available: number;
    emergency_escalation_ready: boolean;
  };
  voice_assistant_ready: boolean;
  recent_consultations: RecentConsultationSummary[];
  guidance_tips: GuidanceTip[];
}

export interface MessageItem {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface ConsultationDetail {
  id: string;
  created_at: string;
  language: string;
  chief_complaint: string;
  stage: string;
  risk_level: string;
  is_emergency: boolean;
  welcome_message?: string;
  messages: MessageItem[];
  summary?: {
    chief_complaint: string;
    duration: string;
    risk_assessment: string;
    red_flags_present: boolean;
    recommended_action: string;
  };
}

export interface Doctor {
  id: string;
  name: string;
  specialty: string;
  qualification: string;
  experience_years: number;
  hospital_or_clinic: string;
  city: string;
  languages: string;
  teleconsult_available: boolean;
  in_person_available: boolean;
  fee_inr: number;
  rating: string;
}

export interface DoctorListResponse {
  total: number;
  doctors: Doctor[];
  cities: string[];
  specialties: string[];
}
