import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const LOGIN_PATH = import.meta.env.VITE_API_LOGINPATH || '/api/v1/auth/login';
const TASKS_URL = `${BASE_URL}${LOGIN_PATH}`;

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(TASKS_URL, {
        email,
        password,
      });
      login(response.data.access_token);
    } catch (err: unknown) {
      console.error('Erro de login:', err);
      alert('Login falhou!');
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded shadow-md w-96 space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">TaskFlow Login</h2>
        <input
          type="email"
          className="w-full px-4 py-2 border rounded"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="w-full px-4 py-2 border rounded"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Entrar
        </button>
      </form>
    </div>
  );
};

export default Login;
