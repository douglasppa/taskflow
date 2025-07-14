import type { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
  return (
    <div className="bg-white shadow p-4 rounded-md border border-gray-200">
      <h3 className="text-lg font-semibold text-black">{task.title}</h3>
      <p className="text-gray-700 mt-1">{task.description}</p>
    </div>
  );
}
