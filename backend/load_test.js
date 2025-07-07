import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // sobe para 20 VUs em 30s
    { duration: '30s', target: 50 },   // aumenta para 50 VUs em mais 30s
    { duration: '1m', target: 100 },   // sustenta 100 VUs por 1 min
    { duration: '30s', target: 0 },    // reduz para 0 (cooldown)
  ],
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

  // Menor intervalo entre requisições
  sleep(0.1);
}
