import { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';
import { GoogleLogin } from '@react-oauth/google';
import type { CredentialResponse } from '@react-oauth/google';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';

const LOGIN_PATH = import.meta.env.VITE_API_LOGIN_PATH || '/api/v1/auth/login';
const TASKS_URL = `${BASE_URL}${LOGIN_PATH}`;

const GOOGLE_PATH =
  import.meta.env.VITE_API_GOOGLE_PATH || '/api/v1/auth/google';
const GOOGLE_URL = `${BASE_URL}${GOOGLE_PATH}`;

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
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md space-y-5"
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800">
          <span className="text-blue-600 font-bold">TaskFlow</span> Login
        </h2>

        <input
          type="email"
          className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
        >
          Entrar
        </button>

        <div className="text-sm text-gray-500 text-left">
          Esqueceu sua senha?{' '}
          <a href="#" className="text-blue-600 hover:underline">
            Recuperar acesso
          </a>
        </div>

        <div className="text-sm text-gray-500 text-left">
          Não tem uma conta?{' '}
          <a href="/register" className="text-blue-600 hover:underline">
            Criar conta
          </a>
        </div>

        <div className="border-t pt-4">
          <p className="text-center text-sm text-gray-500 mb-2">Ou</p>
          <div className="flex justify-center gap-4">
            <GoogleLogin
              onSuccess={async (credentialResponse: CredentialResponse) => {
                const idToken = credentialResponse.credential;
                if (!idToken) return;

                try {
                  const res = await axios.post(GOOGLE_URL, {
                    token: idToken,
                  });
                  login(res.data.access_token);
                } catch (error) {
                  console.error('Erro no login com Google:', error);
                  alert('Falha ao logar com Google');
                }
              }}
              onError={() => {
                alert('Erro ao autenticar com Google');
              }}
              useOneTap={false}
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default Login;
