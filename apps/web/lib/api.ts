import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Internship {
  id: string;
  slug: string;
  title: string;
  company_name: string;
  company_trust_score?: number;
  city?: string;
  state?: string;
  location_text: string;
  work_mode: 'remote' | 'hybrid' | 'onsite';
  domain_slug: string;
  stipend_min?: number;
  stipend_max?: number;
  stipend_text?: string;
  apply_by?: string;
  is_expiring_soon?: boolean;
  trust_score: number;
  verification_status: 'verified' | 'needs_review' | 'draft' | 'pending' | 'rejected';
  duration_text?: string;
  freshness_bucket?: string;
  skills: string[];
  posted_at?: string;
}

export interface FetchInternshipsParams {
  region: string;
  domain: string;
  work_mode?: string;
  freshness?: string;
  verified_only?: boolean;
  high_trust?: boolean;
  sort?: string;
  limit?: number;
  cursor?: string;
}

export interface FetchInternshipsResponse {
  success: boolean;
  data: Internship[];
  meta: {
    next_cursor?: string;
    total?: number;
  };
}

export const fetchInternships = async (params: FetchInternshipsParams): Promise<FetchInternshipsResponse> => {
  const { data } = await api.get('/api/v1/internships', { params });
  return data;
};

export const fetchInternshipDetail = async (slug: string): Promise<{ success: boolean; data: Internship }> => {
  const { data } = await api.get(`/api/v1/internships/${slug}`);
  return data;
};

export default api;
