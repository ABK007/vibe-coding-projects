import { Todo, TodoCreate, TodoUpdate, TodoListResponse } from "@/types/todo";

const BASE_URL = "https://unsought-earline-synclastic.ngrok-free.dev/api/v1";

export const todoApi = {
  async getAll(params?: {
    skip?: number;
    limit?: number;
    completed?: boolean;
    priority?: string;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<TodoListResponse> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value));
        }
      });
    }
    
    const queryString = queryParams.toString();
    const url = queryString ? `${BASE_URL}/todos/?${queryString}` : `${BASE_URL}/todos/`;
    
    const response = await fetch(url, {
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
    });
    if (!response.ok) throw new Error("Failed to fetch todos");
    return response.json();
  },

  async getById(id: number): Promise<Todo> {
    const response = await fetch(`${BASE_URL}/todos/${id}`, {
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
    });
    if (!response.ok) throw new Error("Failed to fetch todo");
    return response.json();
  },

  async create(todo: TodoCreate): Promise<Todo> {
    const response = await fetch(`${BASE_URL}/todos/`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
      },
      body: JSON.stringify(todo),
    });
    if (!response.ok) throw new Error("Failed to create todo");
    return response.json();
  },

  async update(id: number, todo: TodoUpdate): Promise<Todo> {
    const response = await fetch(`${BASE_URL}/todos/${id}`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
      },
      body: JSON.stringify(todo),
    });
    if (!response.ok) throw new Error("Failed to update todo");
    return response.json();
  },

  async toggle(id: number): Promise<Todo> {
    const response = await fetch(`${BASE_URL}/todos/${id}/toggle`, {
      method: "PATCH",
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
    });
    if (!response.ok) throw new Error("Failed to toggle todo");
    return response.json();
  },

  async delete(id: number): Promise<{ message: string }> {
    const response = await fetch(`${BASE_URL}/todos/${id}`, {
      method: "DELETE",
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
    });
    if (!response.ok) throw new Error("Failed to delete todo");
    return response.json();
  },

  async deleteAllCompleted(): Promise<{ message: string }> {
    const response = await fetch(`${BASE_URL}/todos/completed/all`, {
      method: "DELETE",
      headers: {
        "ngrok-skip-browser-warning": "true",
      },
    });
    if (!response.ok) throw new Error("Failed to delete completed todos");
    return response.json();
  },
};
