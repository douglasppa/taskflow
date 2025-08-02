import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { useContext } from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { AuthProvider } from '../../providers/AuthProvider';

// Mock de decodeToken
vi.mock('../../utils/tokenUtils', () => ({
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  decodeToken: (_: string) => ({
    sub: '123',
    email: 'user@test.com',
  }),
}));

const TestComponent = () => {
  const { user, isAuthenticated, login, logout, token } =
    useContext(AuthContext);

  return (
    <div>
      <p>Usuário: {user?.email || 'Nenhum'}</p>
      <p>Token: {token || 'Nenhum'}</p>
      <p>Autenticado: {isAuthenticated ? 'Sim' : 'Não'}</p>
      <button onClick={() => login('mock-token')}>Fazer login</button>
      <button onClick={logout}>Fazer logout</button>
    </div>
  );
};

const renderWithAuthProvider = (initialPath = '/') =>
  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route
          path="*"
          element={
            <AuthProvider>
              <TestComponent />
            </AuthProvider>
          }
        />
      </Routes>
    </MemoryRouter>,
  );

describe('AuthProvider', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('carrega token do localStorage ao iniciar', async () => {
    localStorage.setItem('token', 'mock-token');
    renderWithAuthProvider();

    await waitFor(() => {
      expect(screen.getByText(/Usuário: user@test.com/i)).toBeInTheDocument();
      expect(screen.getByText(/Autenticado: Sim/i)).toBeInTheDocument();
    });
  });

  it('realiza login corretamente', async () => {
    renderWithAuthProvider();

    screen.getByText('Fazer login').click();

    await waitFor(() => {
      expect(localStorage.getItem('token')).toBe('mock-token');
      expect(screen.getByText(/Usuário: user@test.com/i)).toBeInTheDocument();
      expect(screen.getByText(/Autenticado: Sim/i)).toBeInTheDocument();
    });
  });

  it('realiza logout corretamente', async () => {
    localStorage.setItem('token', 'mock-token');
    renderWithAuthProvider();

    await waitFor(() => {
      expect(screen.getByText(/Usuário: user@test.com/i)).toBeInTheDocument();
    });

    screen.getByText('Fazer logout').click();

    await waitFor(() => {
      expect(localStorage.getItem('token')).toBeNull();
      expect(screen.getByText(/Usuário: Nenhum/i)).toBeInTheDocument();
      expect(screen.getByText(/Autenticado: Não/i)).toBeInTheDocument();
    });
  });
});
