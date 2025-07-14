import { Link } from 'react-router-dom';
import AuthenticatedLayout from '../components/AuthenticatedLayout';

export default function Dashboard() {
  return (
    <AuthenticatedLayout>
      <h2 className="text-2xl font-bold mb-4 text-black">
        Bem-vindo ao TaskFlow
      </h2>
      <p className="mb-6 text-black">Esta é sua área autenticada.</p>

      <Link
        to="/tasks"
        className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Ver Minhas Tarefas
      </Link>
    </AuthenticatedLayout>
  );
}
