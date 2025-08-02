import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import AuthenticatedLayout from '../../layouts/AuthenticatedLayout';

// Mock do useAuth
const logoutMock = vi.fn();
vi.mock('../../hooks/useAuth', () => ({
  useAuth: () => ({
    logout: logoutMock,
    user: { email: 'user@test.com' },
  }),
}));

// Mock da versão
vi.mock('../../utils/version', () => ({
  frontendVersion: '1.0.0',
}));

const TestPage = () => <div>Conteúdo protegido</div>;

const renderWithLayout = (initialPath = '/dashboard') =>
  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route
          path="*"
          element={
            <AuthenticatedLayout>
              <TestPage />
            </AuthenticatedLayout>
          }
        />
      </Routes>
    </MemoryRouter>,
  );

describe('AuthenticatedLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('exibe cabeçalho com título, navegação e botão de logout', () => {
    renderWithLayout();

    expect(screen.getByText(/TaskFlow/i)).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: /Dashboard/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Tarefas/i })).toBeInTheDocument();
    expect(screen.getByText(/Logout/i)).toBeInTheDocument();
  });

  it('destaca o item ativo da navegação com base na URL', () => {
    renderWithLayout('/tasks');

    const tarefasLink = screen.getByRole('link', { name: /Tarefas/i });
    expect(tarefasLink).toHaveClass('text-blue-600');
  });

  it('mostra o e-mail do usuário e a versão do frontend', () => {
    renderWithLayout();

    expect(screen.getByText(/user@test.com/i)).toBeInTheDocument();
    expect(screen.getByText(/v1.0.0/i)).toBeInTheDocument();
  });

  it('executa logout ao clicar no botão', () => {
    renderWithLayout();

    const logoutButton = screen.getByRole('button', { name: /logout/i });
    fireEvent.click(logoutButton);

    expect(logoutMock).toHaveBeenCalled();
  });

  it('renderiza o conteúdo passado como children', () => {
    renderWithLayout();
    expect(screen.getByText(/conteúdo protegido/i)).toBeInTheDocument();
  });
});
