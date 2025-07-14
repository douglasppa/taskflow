import axios from 'axios';
import type { Task } from '../types/task';
import { getToken } from '../utils/tokenUtils';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const TASKS_PATH = import.meta.env.VITE_API_TASKS_PATH || '/api/v1/tasks';
const TASKS_URL = `${BASE_URL}${TASKS_PATH}`;

export async function getTasks(skip = 0, limit = 10): Promise<Task[]> {
  const token = getToken();
  const response = await axios.get(`${TASKS_URL}?skip=${skip}&limit=${limit}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}

export async function createTask(task: {
  title: string;
  description: string;
}): Promise<void> {
  const token = getToken();
  await axios.post(TASKS_URL, task, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function updateTask(
  id: number,
  task: { title: string; description: string },
): Promise<void> {
  const token = getToken();
  await axios.put(`${TASKS_URL}/${id}`, task, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function deleteTask(id: number): Promise<void> {
  const token = getToken();
  await axios.delete(`${TASKS_URL}/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
