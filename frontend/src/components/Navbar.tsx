import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white border-b shadow-sm px-6 py-3 flex justify-between items-center">
      <div className="flex gap-6 text-sm font-medium text-gray-700">
        <Link to="/dashboard" className="hover:text-blue-600">
          Dashboard
        </Link>
        <Link to="/tasks" className="hover:text-blue-600">
          Tarefas
        </Link>
      </div>
      <button
        onClick={handleLogout}
        className="text-sm text-red-600 hover:text-red-700"
      >
        Sair
      </button>
    </nav>
  );
}
