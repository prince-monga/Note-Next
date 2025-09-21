export interface User {
  id: number;
  username: string;
  role: 'child' | 'parent';
  parent_id?: number;
}

export interface Child {
  id: number;
  username: string;
  email: string;
}

export interface Folder {
  id: number;
  name: string;
  owner_id: number;
  created_at: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  tags: string;
  is_todo: boolean;
  is_completed: boolean;
  folder_id?: number;
  owner_id: number;
  created_at: string;
  updated_at: string;
}