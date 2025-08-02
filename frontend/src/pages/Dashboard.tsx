import { Link } from 'react-router-dom';
import { LayoutDashboard, ListChecks, User } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="w-full max-w-md mx-auto mt-10 text-center">
      <div className="flex items-center justify-center gap-2 mb-4">
        <LayoutDashboard className="w-6 h-6 text-blue-600" />
        <h2 className="text-2xl font-bold text-gray-800">
          Bem-vindo ao TaskFlow
        </h2>
      </div>

      <p
        data-testid="user-email"
        className="mb-4 text-gray-600 text-sm flex items-center justify-center gap-2"
      >
        <User className="w-4 h-4 text-gray-500" />
        {user?.email}
      </p>

      <p className="mb-6 text-gray-600 text-sm">
        Esta é sua área autenticada. Gerencie suas tarefas com facilidade!
      </p>

      <div className="flex flex-col sm:flex-row justify-center gap-4">
        <Link
          to="/tasks"
          className="inline-flex items-center justify-center gap-2 px-5 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
        >
          <ListChecks className="w-4 h-4" />
          Ver Minhas Tarefas
        </Link>
      </div>
    </div>
  );
}
