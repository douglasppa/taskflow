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
import { Pencil, Trash2, PlusCircle, ListChecks } from 'lucide-react';

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

  function renderTaskList() {
    if (loading) return <p>Carregando...</p>;
    if (tasks.length === 0)
      return (
        <p className="text-gray-600 text-center mt-8">
          Nenhuma tarefa encontrada.
        </p>
      );

    return (
      <div className="space-y-4">
        {tasks.map((task) => (
          <div key={task.id} className="flex items-start gap-2 group">
            <TaskCard task={task} />

            <div className="flex flex-col gap-2 pt-1">
              <button
                onClick={() => {
                  setEditingTask(task);
                  setModalOpen(true);
                }}
                className="p-2 text-blue-600 hover:text-blue-800 hover:bg-blue-100 rounded-md transition"
                title="Editar"
              >
                <Pencil className="w-4 h-4" />
              </button>

              <button
                onClick={() => handleDelete(task.id)}
                disabled={loadingDeleteId === task.id}
                className={`p-2 rounded-md transition
                    ${
                      loadingDeleteId === task.id
                        ? 'text-gray-400 animate-pulse'
                        : 'text-red-600 hover:text-red-800 hover:bg-red-100'
                    }
                  `}
                title="Excluir"
              >
                {loadingDeleteId === task.id ? (
                  <svg
                    className="animate-spin h-4 w-4 text-red-600"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 100 8v4a8 8 0 01-8-8z"
                    />
                  </svg>
                ) : (
                  <Trash2 className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        ))}
      </div>
    );
  }

  function renderPagination() {
    return (
      <div className="flex justify-between items-center mt-6">
        <button
          onClick={() => fetchTasks(currentPage - 1)}
          disabled={currentPage === 0}
          className={`px-4 py-2 rounded text-sm transition ${
            currentPage === 0
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-gray-300 text-gray-800 hover:bg-gray-400'
          }`}
        >
          Anterior
        </button>

        <span className="text-sm text-gray-600">Página {currentPage + 1}</span>

        <button
          onClick={() => fetchTasks(currentPage + 1)}
          disabled={tasks.length < tasksPerPage}
          className={`px-4 py-2 rounded text-sm transition ${
            tasks.length < tasksPerPage
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-gray-300 text-gray-800 hover:bg-gray-400'
          }`}
        >
          Próxima
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto mt-8 px-4">
      <h1 className="text-2xl font-bold mb-4 text-gray-800 flex items-center gap-2">
        <ListChecks className="w-6 h-6 text-blue-600" />
        Minhas Tarefas
      </h1>

      {renderTaskList()}
      {!loading && renderPagination()}

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

      <PlusCircle
        onClick={() => setModalOpen(true)}
        className="fixed bottom-6 right-6 w-12 h-12 text-white bg-blue-600 p-2 rounded-full shadow-lg hover:bg-blue-700 cursor-pointer"
      />
    </div>
  );
}
