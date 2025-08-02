import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const REGISTER_PATH =
  import.meta.env.VITE_API_REGISTER_PATH || '/api/v1/auth/register';
const REGISTER_URL = `${BASE_URL}${REGISTER_PATH}`;

const registerSchema = z.object({
  email: z.email({ message: 'E-mail inválido' }),
  password: z
    .string()
    .min(6, { message: 'Senha deve ter no mínimo 6 caracteres' }),
});

type RegisterFormData = z.infer<typeof registerSchema>;

export default function Register() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError('');
    try {
      await axios.post(REGISTER_URL, data);
      navigate('/');
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || 'Erro ao criar conta');
      } else {
        setError('Erro desconhecido');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md space-y-5"
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800">
          <span className="text-blue-600 font-bold">TaskFlow</span> Registro
        </h2>

        <div>
          <input
            type="email"
            {...register('email')}
            placeholder="E-mail"
            className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          {errors.email && (
            <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>

        <div>
          <div className="relative w-full">
            <input
              type={showPassword ? 'text' : 'password'}
              {...register('password')}
              placeholder="Senha"
              className="w-full border border-gray-300 rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowPassword((prev) => !prev)}
              aria-label={showPassword ? 'Esconder senha' : 'Mostrar senha'}
              title={showPassword ? 'Esconder senha' : 'Mostrar senha'}
            >
              {showPassword ? (
                <Eye className="h-5 w-5 text-gray-500" />
              ) : (
                <EyeOff className="h-5 w-5 text-gray-500" />
              )}
            </button>
          </div>
          {errors.password && (
            <p className="text-red-600 text-sm mt-1">
              {errors.password.message}
            </p>
          )}
        </div>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
        >
          {isSubmitting ? 'Criando conta...' : 'Registrar'}
        </button>

        <div className="text-sm text-gray-500 text-left">
          Já tem uma conta?{' '}
          <Link to="/" className="text-blue-600 hover:underline">
            Entrar
          </Link>
        </div>
      </form>
    </div>
  );
}
