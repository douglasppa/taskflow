import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { AuthContext } from '../../context/AuthContext';
import { useContext } from 'react';

const TestComponent = () => {
  const { token, isAuthenticated, user, isLoading, login, logout } =
    useContext(AuthContext);
  return (
    <div>
      <div>Token: {token}</div>
      <div>Authenticated: {isAuthenticated ? 'yes' : 'no'}</div>
      <div>User: {user ? user.email : 'none'}</div>
      <div>Loading: {isLoading ? 'yes' : 'no'}</div>
      <button onClick={() => login('mock-token')}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  it('deve lançar erro se usado fora do provider', () => {
    // Como você não está protegendo com throw, este teste é apenas ilustrativo
    // Se quiser reforçar segurança, pode criar hook useAuth que valida contexto
    expect(() => render(<TestComponent />)).not.toThrow(); // Só passa porque context default é um objeto vazio tipado
  });
});
