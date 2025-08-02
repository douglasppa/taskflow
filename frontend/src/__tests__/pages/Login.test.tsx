import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from '../../pages/Login';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import { GoogleOAuthProvider } from '@react-oauth/google';

// Mock do hook useAuth
const loginMock = vi.fn();
vi.mock('../../hooks/useAuth', () => ({
  useAuth: () => ({ login: loginMock }),
}));

// Mock do axios
vi.mock('axios');
const mockedAxios = axios as unknown as { post: ReturnType<typeof vi.fn> };

const renderWithRouter = () =>
  render(
    <GoogleOAuthProvider clientId="test-client-id">
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    </GoogleOAuthProvider>,
  );

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza campos de e-mail e senha', () => {
    renderWithRouter();
    expect(screen.getByPlaceholderText(/e-mail/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  it('envia o formulário com sucesso e chama login', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: { access_token: 'token123' },
    });

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/e-mail/i), {
      target: { value: 'teste@email.com' },
    });
    fireEvent.change(screen.getByPlaceholderText(/senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalled();
      expect(loginMock).toHaveBeenCalledWith('token123');
    });
  });

  it('mostra alerta se login falhar', async () => {
    const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => {});
    mockedAxios.post.mockRejectedValueOnce(new Error('Erro'));

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/e-mail/i), {
      target: { value: 'teste@email.com' },
    });
    fireEvent.change(screen.getByPlaceholderText(/senha/i), {
      target: { value: 'errado' },
    });

    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    await waitFor(() => {
      expect(alertMock).toHaveBeenCalledWith('Login falhou!');
    });
  });

  it('abre o modal de recuperação de senha ao clicar no botão', () => {
    renderWithRouter();

    const recuperarBtn = screen.getByRole('button', {
      name: /recuperar acesso/i,
    });

    fireEvent.click(recuperarBtn);

    expect(screen.getAllByText(/recuperar acesso/i)[0]).toBeInTheDocument();
  });

  it('possui link para criar conta', () => {
    renderWithRouter();
    const criarContaLink = screen.getByRole('link', {
      name: /criar conta/i,
    });
    expect(criarContaLink).toHaveAttribute('href', '/register');
  });

  it('não envia o formulário se os campos estiverem vazios', async () => {
    renderWithRouter();

    // Clica no botão sem preencher os campos
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    // Aguarda e garante que o loginMock não foi chamado
    await waitFor(() => {
      expect(loginMock).not.toHaveBeenCalled();
      expect(mockedAxios.post).not.toHaveBeenCalled();
    });
  });
});
