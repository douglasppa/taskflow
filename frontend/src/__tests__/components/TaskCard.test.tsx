import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import TaskCard from '../../components/TaskCard';
import type { Task } from '../../types/task';

describe('TaskCard', () => {
  const mockTask: Task = {
    id: 1,
    title: 'Título de teste',
    description: 'Descrição da tarefa teste',
    owner_id: 42,
  };

  it('renderiza o título e a descrição da tarefa', () => {
    render(<TaskCard task={mockTask} />);

    expect(screen.getByText(/Título de teste/i)).toBeInTheDocument();
    expect(screen.getByText(/Descrição da tarefa teste/i)).toBeInTheDocument();
  });
});
