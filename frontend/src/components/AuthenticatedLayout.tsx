import type { ReactNode } from 'react';
import { useAuth } from '../hooks/useAuth';
import { frontendVersion } from '../utils/version';

const AuthenticatedLayout = ({ children }: { children: ReactNode }) => {
  const { logout, user } = useAuth();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow">
        <h1 className="text-xl font-semibold">TaskFlow</h1>
        <p className="text-xs opacity-75">Frontend {frontendVersion}</p>
        <div className="flex items-center gap-4">
          <span className="text-sm italic">User: {user?.email}</span>
          <button
            onClick={logout}
            className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-blue-100 transition"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="flex-1 p-6">{children}</main>
    </div>
  );
};

export default AuthenticatedLayout;
