import { render, screen } from '@testing-library/react';
import Dashboard from '../../pages/Dashboard';
import { MemoryRouter } from 'react-router-dom';
import { vi, describe, it, expect } from 'vitest';
import { AuthContext } from '../../context/AuthContext';
import { within } from '@testing-library/dom';

describe('Dashboard', () => {
  const userMock = {
    id: '123',
    email: 'teste@exemplo.com',
  };

  const authContextValue = {
    user: userMock,
    token: 'fake-token',
    isLoading: false,
    isAuthenticated: true,
    login: vi.fn(),
    logout: vi.fn(),
  };

  it('exibe título, e-mail do usuário e link de tarefas', () => {
    render(
      <AuthContext.Provider value={authContextValue}>
        <MemoryRouter>
          <Dashboard />
        </MemoryRouter>
      </AuthContext.Provider>,
    );

    expect(
      screen.getByRole('heading', { name: /bem-vindo ao taskflow/i }),
    ).toBeInTheDocument();

    const emailWrapper = screen.getByTestId('user-email');
    expect(within(emailWrapper).getByText(userMock.email)).toBeInTheDocument();

    expect(
      screen.getByText(/esta é sua área autenticada/i),
    ).toBeInTheDocument();

    const tarefasLink = screen.getByRole('link', {
      name: /ver minhas tarefas/i,
    });
    expect(tarefasLink).toHaveAttribute('href', '/tasks');
  });
});
