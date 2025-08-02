import type { ReactNode } from 'react';
import { useAuth } from '../hooks/useAuth';
import { frontendVersion } from '../utils/version';
import { Link, useLocation } from 'react-router-dom';
import { LogOut } from 'lucide-react';

interface Props {
  children: ReactNode;
}

export default function AuthenticatedLayout({ children }: Readonly<Props>) {
  const { logout, user } = useAuth();
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'Tarefas', path: '/tasks' },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white border-b shadow-sm px-4 py-2 sm:px-6 sm:py-4 flex justify-between items-center">
        <div className="flex items-center gap-4 sm:gap-8">
          <h1 className="text-xl font-bold text-blue-600">TaskFlow</h1>

          <nav className="flex gap-4 sm:gap-6 text-sm font-medium">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`relative transition text-gray-700 hover:text-blue-600 ${
                  location.pathname === item.path
                    ? 'text-blue-600 font-semibold after:absolute after:-bottom-1 after:left-0 after:h-0.5 after:w-full after:bg-blue-600'
                    : ''
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="flex items-center gap-2 sm:gap-4 text-sm text-gray-600">
          <span className="italic hidden sm:inline">User: {user?.email}</span>
          <span className="hidden sm:inline text-xs opacity-60">
            v{frontendVersion}
          </span>

          <button
            onClick={logout}
            className="flex items-center gap-1.5 bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700 transition text-sm"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
