import axios from 'axios';
import { Folder, Note } from './types';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: (username: string, email: string, password: string, role: string, parent_id?: number, child_ids?: number[]) =>
    api.post('/signup', { username, email, password, role, parent_id, child_ids }),
  
  login: (username: string, password: string) =>
    api.post('/login', { username, password }),
  
  getAvailableChildren: () => api.get('/available-children'),
};

// Children API
export const childrenAPI = {
  getAll: () => {
    const token = localStorage.getItem('token');
    return api.get('/children', { params: { token } });
  },
};

// Folders API
export const foldersAPI = {
  getAll: (childId?: number) => {
    const token = localStorage.getItem('token');
    return api.get<Folder[]>('/folders', { params: { child_id: childId, token } });
  },
  create: (name: string) => api.post<Folder>('/folders', { name }),
  delete: (id: number) => api.delete(`/folders/${id}`),
};

// Notes API
export const notesAPI = {
  getAll: (folderId?: number, childId?: number) => {
    const token = localStorage.getItem('token');
    return api.get<Note[]>('/notes', { params: { folder_id: folderId, child_id: childId, token } });
  },
  create: (note: { title: string; content: string; tags?: string; is_todo?: boolean; folder_id?: number }) => {
    const token = localStorage.getItem('token');
    return api.post<Note>('/notes', { ...note, token });
  },
  update: (id: number, note: Partial<Note>) => api.put<Note>(`/notes/${id}`, note),
  delete: (id: number) => api.delete(`/notes/${id}`),
};