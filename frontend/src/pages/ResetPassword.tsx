import { useSearchParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import axios from 'axios';
import { z } from 'zod';
import { Link } from 'react-router-dom';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const RESET_PATH =
  import.meta.env.VITE_API_RESET_PASSWORD_PATH || '/api/v1/auth/reset-password';
const RESET_URL = `${BASE_URL}${RESET_PATH}`;

const schema = z.object({
  new_password: z
    .string()
    .min(6, 'A nova senha deve ter pelo menos 6 caracteres'),
});

type ResetFormData = z.infer<typeof schema>;

const ResetPassword = () => {
  const [params] = useSearchParams();
  const token = params.get('token');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetFormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: ResetFormData) => {
    if (!token) {
      setMessage('Token ausente na URL.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(RESET_URL, {
        token,
        new_password: data.new_password,
      });
      setMessage(response.data.message || 'Senha redefinida com sucesso!');
    } catch (error) {
      console.error('Erro ao redefinir senha:', error);
      setMessage('Não foi possível redefinir a senha.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md space-y-5"
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800">
          <span className="text-blue-600 font-bold">TaskFlow</span> Redefinir
          senha
        </h2>

        {message ? (
          <>
            <p className="text-center text-gray-600">{message}</p>
            <Link
              to="/"
              className="block w-full mt-4 text-center bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
            >
              Voltar ao login
            </Link>
          </>
        ) : (
          <>
            <input
              type="password"
              placeholder="Nova senha"
              className={`w-full border ${
                errors.new_password ? 'border-red-500' : 'border-gray-300'
              } rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none`}
              {...register('new_password')}
              disabled={loading}
            />
            <p className="text-sm text-gray-500 mt-1">
              *A senha deve conter no mínimo 6 caracteres.
            </p>
            {errors.new_password && (
              <p className="text-red-500 text-sm">
                {errors.new_password.message}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-2 rounded-md text-white transition ${
                loading
                  ? 'bg-blue-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {loading ? 'Enviando...' : 'Redefinir'}
            </button>

            <div className="text-sm text-gray-500 text-left">
              <Link
                to="/"
                className="block w-full mt-4 text-center bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
              >
                Voltar ao login
              </Link>
            </div>
          </>
        )}
      </form>
    </div>
  );
};

export default ResetPassword;
