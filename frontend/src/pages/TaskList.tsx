import { useEffect, useState } from 'react';
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
} from '../services/taskService';
import TaskCard from '../components/TaskCard';
import TaskFormModal from '../components/TaskFormModal';
import type { Task } from '../types/task';
import type { TaskFormData } from '../components/TaskForm';
import toast from 'react-hot-toast';

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loadingDeleteId, setLoadingDeleteId] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState(0);
  const tasksPerPage = 10;

  useEffect(() => {
    fetchTasks(0);
  }, []);

  async function fetchTasks(page = 0) {
    setLoading(true);
    try {
      const skip = page * tasksPerPage;
      const data = await getTasks(skip, tasksPerPage);
      setTasks(data);
      setCurrentPage(page);
    } catch (error) {
      console.error('Erro ao buscar tarefas:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(data: TaskFormData) {
    try {
      await createTask(data);
      toast.success('Tarefa criada com sucesso!');
      setModalOpen(false);
      await fetchTasks(currentPage);
    } catch (error) {
      console.error('Erro ao criar tarefa:', error);
      toast.error('Erro ao criar tarefa.');
    }
  }

  async function handleUpdate(data: TaskFormData) {
    if (!editingTask) return;

    try {
      await updateTask(editingTask.id, data);
      toast.success('Tarefa atualizada!');
      setModalOpen(false);
      setEditingTask(null);
      await fetchTasks(currentPage);
    } catch (error) {
      console.error('Erro ao atualizar tarefa:', error);
      toast.error('Erro ao atualizar tarefa.');
    }
  }

  async function handleDelete(id: number) {
    const confirm = window.confirm(
      'Tem certeza que deseja excluir esta tarefa?',
    );
    if (!confirm) return;

    try {
      setLoadingDeleteId(id);
      await deleteTask(id);
      toast.success('Tarefa excluída!');
      await fetchTasks(currentPage);
    } catch (error) {
      console.error('Erro ao excluir tarefa:', error);
      toast.error('Erro ao excluir tarefa.');
    } finally {
      setLoadingDeleteId(null);
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-8 px-4">
      <h1 className="text-2xl font-bold mb-4">Minhas Tarefas</h1>

      {loading ? (
        <p>Carregando...</p>
      ) : tasks.length === 0 ? (
        <p>Nenhuma tarefa encontrada.</p>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onEdit={(t) => {
                setEditingTask(t);
                setModalOpen(true);
              }}
              onDelete={handleDelete}
              loadingDeleteId={loadingDeleteId}
            />
          ))}
        </div>
      )}

      {!loading && (
        <div className="flex justify-between items-center mt-6">
          <button
            onClick={() => fetchTasks(currentPage - 1)}
            disabled={currentPage === 0}
            className="px-4 py-2 rounded bg-gray-200 text-sm disabled:opacity-50"
          >
            Anterior
          </button>

          <span className="text-sm">Página {currentPage + 1}</span>

          <button
            onClick={() => fetchTasks(currentPage + 1)}
            disabled={tasks.length < tasksPerPage}
            className="px-4 py-2 rounded bg-gray-200 text-sm disabled:opacity-50"
          >
            Próxima
          </button>
        </div>
      )}

      <TaskFormModal
        isOpen={isModalOpen}
        onClose={() => {
          setModalOpen(false);
          setEditingTask(null);
        }}
        onSubmit={editingTask ? handleUpdate : handleCreate}
        initialData={
          editingTask
            ? {
                title: editingTask.title,
                description: editingTask.description,
              }
            : undefined
        }
        editMode={!!editingTask}
      />

      <button
        onClick={() => setModalOpen(true)}
        className="fixed bottom-6 right-6 bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-blue-700"
      >
        Nova Tarefa
      </button>
    </div>
  );
}
