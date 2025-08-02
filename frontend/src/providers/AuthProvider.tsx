import type { ReactNode } from 'react';
import { useEffect, useState, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { decodeToken } from '../utils/tokenUtils';
import { AuthContext } from '../context/AuthContext';
import type { AuthContextType } from '../context/AuthContext';

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<{ id: string; email: string } | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      const decoded = decodeToken(storedToken);
      setUser({ id: decoded.sub, email: decoded.email });
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(
    (newToken: string) => {
      localStorage.setItem('token', newToken);
      setToken(newToken);
      const decoded = decodeToken(newToken);
      setUser({ id: decoded.sub, email: decoded.email });
      navigate('/dashboard');
    },
    [navigate],
  );

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    navigate('/');
  }, [navigate]);

  const value: AuthContextType = useMemo(
    () => ({
      token,
      isAuthenticated: !!token,
      user,
      login,
      logout,
      isLoading,
    }),
    [token, user, login, logout, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
