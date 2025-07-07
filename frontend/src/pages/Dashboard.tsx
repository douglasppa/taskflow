import AuthenticatedLayout from '../components/AuthenticatedLayout';

const Dashboard = () => {
  return (
    <AuthenticatedLayout>
      <h2 className="text-2xl font-bold mb-4">Bem-vindo ao TaskFlow</h2>
      <p>Esta é sua área autenticada.</p>
    </AuthenticatedLayout>
  );
};

export default Dashboard;
