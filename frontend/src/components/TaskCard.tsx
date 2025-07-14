import type { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
  loadingDeleteId?: number | null;
}

export default function TaskCard({
  task,
  onEdit,
  onDelete,
  loadingDeleteId,
}: TaskCardProps) {
  return (
    <div className="bg-white shadow p-4 rounded-md border border-gray-200 relative">
      <h3 className="text-lg font-semibold text-black">{task.title}</h3>
      <p className="text-gray-700 mt-1">{task.description}</p>

      {onEdit && (
        <button
          onClick={() => onEdit(task)}
          className="absolute top-2 right-2 text-sm text-blue-600 hover:underline"
        >
          Editar
        </button>
      )}
      {onDelete && (
        <button
          onClick={() => onDelete(task.id)}
          className="absolute top-2 right-16 text-sm text-red-600 hover:underline flex items-center gap-1"
          disabled={loadingDeleteId === task.id}
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
          ) : null}
          {loadingDeleteId === task.id ? 'Excluindo...' : 'Excluir'}
        </button>
      )}
    </div>
  );
}
