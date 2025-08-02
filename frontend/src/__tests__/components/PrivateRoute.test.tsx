import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import PrivateRoute from '../../components/PrivateRoute';
import { useAuth } from '../../hooks/useAuth';

// Mock do useAuth
vi.mock('../../hooks/useAuth');

const mockUseAuth = useAuth as ReturnType<typeof vi.fn>;

describe('PrivateRoute', () => {
  const ProtectedContent = () => <div>🔐 Conteúdo Protegido</div>;
  const PublicContent = () => <div>🌐 Página Pública</div>;

  it('mostra "Verificando autenticação..." se isLoading for true', () => {
    mockUseAuth.mockReturnValue({ user: null, token: null, isLoading: true });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <ProtectedContent />
              </PrivateRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText(/verificando autenticação/i)).toBeInTheDocument();
  });

  it('redireciona para / se não houver token ou user', () => {
    mockUseAuth.mockReturnValue({ user: null, token: null, isLoading: false });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/" element={<PublicContent />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <ProtectedContent />
              </PrivateRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText(/página pública/i)).toBeInTheDocument();
  });

  it('renderiza o conteúdo protegido se estiver autenticado', () => {
    mockUseAuth.mockReturnValue({
      user: { id: 1, email: 'teste@exemplo.com' },
      token: 'fake-token',
      isLoading: false,
    });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <ProtectedContent />
              </PrivateRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText(/conteúdo protegido/i)).toBeInTheDocument();
  });
});
