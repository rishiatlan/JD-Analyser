import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface JDAnalysisResponse {
  sections: Array<{
    title: string;
    content: string;
    suggestions: string[];
  }>;
  bias_analysis: {
    biased_terms: string[];
    suggestions: string[];
    inclusivity_score: number;
  };
  readability_analysis: {
    score: number;
    complexity: string;
    suggestions: string[];
  };
  seo_analysis: {
    keywords: string[];
    missing_keywords: string[];
    suggestions: string[];
  };
  overall_score: number;
  improvement_suggestions: string[];
}

export const analyzeJD = async (data: FormData | { content: string }): Promise<JDAnalysisResponse> => {
  try {
    const response = await api.post('/analyze/file', data, {
      headers: data instanceof FormData ? {
        'Content-Type': 'multipart/form-data',
      } : undefined,
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing JD:', error);
    throw error;
  }
};

export const enhanceJD = async (content: string): Promise<{ content: string }> => {
  try {
    const response = await api.post('/enhance', { content });
    return response.data;
  } catch (error) {
    console.error('Error enhancing JD:', error);
    throw error;
  }
}; 