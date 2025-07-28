import { useState } from 'react';
import axios from 'axios';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://wsl.localhost:8000';
const FORGOT_PATH =
  import.meta.env.VITE_API_FORGOT_PASSWORD_PATH ||
  '/api/v1/auth/forgot-password';
const FORGOT_URL = `${BASE_URL}${FORGOT_PATH}`;

interface ForgotPasswordModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const schema = z.object({
  email: z.string().email('E-mail inválido'),
});

type ForgotPasswordFormData = z.infer<typeof schema>;

const ForgotPasswordModal = ({ isOpen, onClose }: ForgotPasswordModalProps) => {
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setLoading(true);
    try {
      const response = await axios.post(FORGOT_URL, { email: data.email });
      setSuccessMessage(
        response.data.message || 'Se o e-mail existir, enviaremos instruções.',
      );
      reset();
    } catch (error) {
      console.error('Erro ao solicitar recuperação:', error);
      setSuccessMessage('Não foi possível enviar as instruções.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    reset();
    setSuccessMessage('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-40 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md relative">
        <button
          className="absolute top-2 right-3 text-gray-500 hover:text-red-500"
          onClick={handleClose}
        >
          ✕
        </button>

        <h3 className="text-xl font-semibold mb-4 text-gray-800">
          Recuperar acesso
        </h3>

        {successMessage ? (
          <p className="text-gray-700">{successMessage}</p>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <input
              type="email"
              placeholder="Digite seu e-mail"
              className={`w-full border ${
                errors.email ? 'border-red-500' : 'border-gray-300'
              } rounded-md px-4 py-2 text-gray-800 focus:ring-2 focus:ring-blue-500 focus:outline-none`}
              {...register('email')}
            />
            {errors.email && (
              <p className="text-red-500 text-sm">{errors.email.message}</p>
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
              {loading ? 'Enviando...' : 'Enviar instruções'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ForgotPasswordModal;
