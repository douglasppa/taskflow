import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

const BASE_URL = 'http://localhost:8000';
const USER = {
  email: 'teste@k6.com',
  password: '123456',
};

export default function () {
  // 1. Tenta criar o usuário (signup)
  const signupRes = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(USER), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(signupRes, {
    'signup status 201 or 409': (r) => r.status === 201 || r.status === 409,
  });

  // 2. Faz login
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify(USER), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status 200': (r) => r.status === 200,
    'token exists': (r) => JSON.parse(r.body).access_token !== undefined,
  });

  const token = JSON.parse(loginRes.body).access_token;

  // 3. Cria uma task
  const payload = {
    title: `Task ${Math.random().toString(36).substring(2, 8)}`,
    description: 'Gerada pelo k6',
  };

  const res = http.post(`${BASE_URL}/api/v1/tasks`, JSON.stringify(payload), {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  check(res, {
    'create task status 201': (r) => r.status === 201,
  });

  sleep(1);
}
