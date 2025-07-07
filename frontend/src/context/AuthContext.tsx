import type { ReactNode } from 'react';
import { createContext, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  user: { id: string; email: string } | null;
  login: (token: string) => void;
  logout: () => void;
}

interface JwtPayload {
  sub: string;
  email: string;
  exp: number;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<{ id: string; email: string } | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      const decoded = jwtDecode<JwtPayload>(storedToken);
      setUser({ id: decoded.sub, email: decoded.email });
    }
  }, []);

  const login = (newToken: string) => {
    console.log(jwtDecode(newToken));
    localStorage.setItem('token', newToken);
    setToken(newToken);
    const decoded = jwtDecode<JwtPayload>(newToken);
    setUser({ id: decoded.sub, email: decoded.email });
    navigate('/dashboard');
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
