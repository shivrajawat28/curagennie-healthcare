export type NavRoute = 'dashboard' | 'new-consultation' | 'history' | 'doctors' | 'hospitals' | 'settings';

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

export interface ClinicalExplanation {
  title: string;
  reasoning: string;
  likelihood_context: string;
}

export interface AssessmentResponse {
  main_concern: string;
  reported_symptoms: string[];
  duration_timeline?: string;
  follow_up_summary: Record<string, string>;
  missing_or_uncertain_info: string[];
  potential_explanations: ClinicalExplanation[];
  warning_signs_screened: string[];
  red_flags_identified: string[];
  is_escalated: boolean;
  suggested_next_steps: string[];
  professional_consultation_recommended: boolean;
  disclaimer: string;
}

export interface QuestionDetail {
  id: string;
  key: string;
  text: string;
  category: string;
  question_index: number;
  total_questions: number;
}

export interface SafetyStatus {
  is_emergency: boolean;
  is_ambiguous: boolean;
  red_flags_detected: string[];
  action_required?: string;
  emergency_contact: string;
}

export type ConversationState =
  | 'INITIAL'
  | 'INTAKE'
  | 'SAFETY_CHECK'
  | 'FOLLOW_UP'
  | 'ASSESSMENT'
  | 'COMPLETED'
  | 'ESCALATED';

export interface EngineResponse {
  session_id: string;
  state: ConversationState;
  assistant_message: string;
  next_question?: QuestionDetail | null;
  safety_status: SafetyStatus;
  normalized_symptoms: string[];
  assessment?: AssessmentResponse | null;
  is_complete: boolean;
  created_at: string;
}

export interface DoctorListResponse {
  total: number;
  doctors: Doctor[];
  cities: string[];
  specialties: string[];
}

export interface Hospital {
  id: string;
  name: string;
  hospital_type: string;
  city: string;
  address: string;
  emergency_24x7: boolean;
  icu_available: boolean;
  helpline: string;
  ambulance_phone: string;
  departments: string[];
  accreditation: string;
  rating: string;
}

export interface HospitalListResponse {
  total: number;
  hospitals: Hospital[];
  cities: string[];
  departments: string[];
}

export interface AppointmentEnquiryPayload {
  doctor_id?: string;
  hospital_id?: string;
  patient_name: string;
  contact_phone: string;
  preferred_mode: 'teleconsult' | 'in-person';
  consultation_session_id?: string;
  notes?: string;
}

export interface AppointmentEnquiryResult {
  enquiry_id: string;
  status: string;
  message: string;
  provider_name: string;
  preferred_mode: string;
  is_demo: boolean;
  notice: string;
}
