export type Priority = "low" | "medium" | "high";

export interface Todo {
  id: number;
  title: string;
  description: string | null;
  priority: Priority;
  completed: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface TodoCreate {
  title: string;
  description?: string;
  priority?: Priority;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: Priority;
}

export interface TodoListResponse {
  total: number;
  todos: Todo[];
}
