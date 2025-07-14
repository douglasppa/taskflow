import axios from 'axios';
import type { Task } from '../types/task';
import { getToken } from '../utils/tokenUtils';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const TASKS_PATH = import.meta.env.VITE_API_TASKS_PATH || '/api/v1/tasks';
const TASKS_URL = `${BASE_URL}${TASKS_PATH}`;

export async function getTasks(): Promise<Task[]> {
  const token = getToken();
  const response = await axios.get(TASKS_URL, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}
