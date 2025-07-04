import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = 'http://localhost:8000';
const USER = {
  email: 'teste@k6.com',
  password: '123456',
};

export default function () {
  // 1. Login
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify(USER), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status 200': (r) => r.status === 200,
  });

  const token = JSON.parse(loginRes.body).access_token;

  // 2. Listagem das tasks
  const tasksRes = http.get(`${BASE_URL}/api/v1/tasks?limit=100`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(tasksRes, {
    'get tasks status 200': (r) => r.status === 200,
  });

  const tasks = JSON.parse(tasksRes.body);

  // 3. Apaga cada task
  for (const task of tasks) {
    const delRes = http.del(`${BASE_URL}/api/v1/tasks/${task.id}`, null, {
      headers: { Authorization: `Bearer ${token}` },
    });

    check(delRes, {
      [`deleted task ${task.id}`]: (r) =>
        r.status === 204 || r.status === 403 || r.status === 404,
    });
  }
}
