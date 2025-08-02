// ResetPassword.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResetPassword from '../../pages/ResetPassword';
import axios from 'axios';
import { BrowserRouter } from 'react-router-dom';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as unknown as { post: ReturnType<typeof vi.fn> };

// Controle dinâmico do token
let tokenValue: string | null = 'test-token';

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useSearchParams: () => [
      new URLSearchParams(tokenValue ? `token=${tokenValue}` : ''),
    ],
  };
});

const renderWithRouter = () =>
  render(
    <BrowserRouter>
      <ResetPassword />
    </BrowserRouter>,
  );

describe('ResetPassword Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    tokenValue = 'test-token'; // valor padrão
  });

  it('renderiza título e campo de nova senha', () => {
    renderWithRouter();
    expect(
      screen.getByRole('heading', { name: /redefinir senha/i }),
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/nova senha/i)).toBeInTheDocument();
  });

  it('valida senha menor que 6 caracteres', async () => {
    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/nova senha/i), {
      target: { value: '123' },
    });

    fireEvent.click(screen.getByRole('button', { name: /redefinir/i }));

    await waitFor(() => {
      expect(screen.getByText(/pelo menos 6 caracteres/i)).toBeInTheDocument();
    });
  });

  it('mostra mensagem de sucesso ao redefinir senha', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: { message: 'Senha redefinida com sucesso!' },
    });

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/nova senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /redefinir/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/senha redefinida com sucesso/i),
      ).toBeInTheDocument();
    });
  });

  it('mostra erro ao falhar na redefinição', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Erro'));

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/nova senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /redefinir/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/não foi possível redefinir/i),
      ).toBeInTheDocument();
    });
  });

  it('mostra mensagem se token estiver ausente', async () => {
    tokenValue = null; // simula URL sem token

    renderWithRouter();

    fireEvent.change(screen.getByPlaceholderText(/nova senha/i), {
      target: { value: '123456' },
    });

    fireEvent.click(screen.getByRole('button', { name: /redefinir/i }));

    await waitFor(() => {
      expect(screen.getByText(/token ausente/i)).toBeInTheDocument();
    });
  });
});
