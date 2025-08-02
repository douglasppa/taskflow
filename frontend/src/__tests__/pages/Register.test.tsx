import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Register from '../../pages/Register';
import { BrowserRouter } from 'react-router-dom';
import axios, { AxiosError } from 'axios';

const navigateMock = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

vi.mock('axios');
const mockedAxios = axios as unknown as {
  post: ReturnType<typeof vi.fn>;
  isAxiosError: (err: unknown) => boolean;
};

mockedAxios.isAxiosError = vi.fn((err: unknown): err is AxiosError => {
  return typeof err === 'object' && err !== null && 'isAxiosError' in err;
});

const renderWithRouter = () => {
  render(
    <BrowserRouter>
      <Register />
    </BrowserRouter>,
  );
};

describe('Register Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza campos e botão de registro', () => {
    renderWithRouter();
    expect(screen.getByPlaceholderText(/e-mail/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/senha/i)).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /registrar/i }),
    ).toBeInTheDocument();
  });

  it('valida campos obrigatórios e exibe mensagens de erro', async () => {
    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /registrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/e-mail inválido/i)).toBeInTheDocument();
      expect(
        screen.getByText(/senha deve ter no mínimo 6 caracteres/i),
      ).toBeInTheDocument();
    });
  });

  it('cadastra com sucesso e redireciona para login', async () => {
    mockedAxios.post.mockResolvedValueOnce({});

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/e-mail/i), {
      target: { value: 'teste@email.com' },
    });
    fireEvent.change(screen.getByPlaceholderText(/senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /registrar/i }));

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalled();
      expect(navigateMock).toHaveBeenCalledWith('/');
    });
  });

  it('exibe erro genérico se erro desconhecido', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Erro qualquer'));

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/e-mail/i), {
      target: { value: 'teste@email.com' },
    });
    fireEvent.change(screen.getByPlaceholderText(/senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /registrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/erro desconhecido/i)).toBeInTheDocument();
    });
  });

  it('possui link para voltar ao login', () => {
    renderWithRouter();
    const loginLink = screen.getByRole('link', {
      name: /entrar/i,
    });
    expect(loginLink).toHaveAttribute('href', '/');
  });
});
