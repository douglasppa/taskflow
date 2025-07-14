import { createContext } from 'react';

export interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  user: { id: string; email: string } | null;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>(
  {} as AuthContextType,
);
