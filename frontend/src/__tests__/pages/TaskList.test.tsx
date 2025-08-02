import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TaskList from '../../pages/TaskList';
import { BrowserRouter } from 'react-router-dom';
import type { SVGProps } from 'react';

// Mocks manuais
const getTasksMock = vi.fn();
const createTaskMock = vi.fn();
const updateTaskMock = vi.fn();
const deleteTaskMock = vi.fn();

vi.mock('../../../services/taskService', () => ({
  getTasks: getTasksMock,
  createTask: createTaskMock,
  updateTask: updateTaskMock,
  deleteTask: deleteTaskMock,
}));

vi.mock('react-hot-toast', () => ({
  default: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

vi.mock('lucide-react', () => ({
  Pencil: () => <svg data-testid="icon-pencil" />,
  Trash2: () => <svg data-testid="icon-trash" />,
  PlusCircle: (props: SVGProps<SVGSVGElement>) => (
    <svg data-testid="icon-plus" {...props} />
  ),
  ListChecks: () => <svg data-testid="icon-list" />,
}));

const renderWithRouter = () =>
  render(
    <BrowserRouter>
      <TaskList />
    </BrowserRouter>,
  );

const mockTasks = [
  { id: 1, title: 'Task 1', description: 'Descrição 1' },
  { id: 2, title: 'Task 2', description: 'Descrição 2' },
];

describe('TaskList Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    getTasksMock.mockResolvedValue(mockTasks);
  });

  it('mostra "Nenhuma tarefa encontrada" se a lista estiver vazia', async () => {
    getTasksMock.mockResolvedValueOnce([]);

    renderWithRouter();

    await waitFor(() => {
      expect(
        screen.getByText(/nenhuma tarefa encontrada/i),
      ).toBeInTheDocument();
    });
  });

  it('permite abrir o modal de criação ao clicar no botão flutuante', async () => {
    renderWithRouter();

    const plusButton = screen.getByTestId('icon-plus');
    fireEvent.click(plusButton);

    await waitFor(() => {
      expect(screen.getAllByText(/tarefa/i).length).toBeGreaterThan(0);
    });
  });

  it('renderiza os botões de paginação e texto da página atual', async () => {
    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByText(/página 1/i)).toBeInTheDocument();
    });

    expect(
      screen.getByRole('button', { name: /próxima/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /anterior/i }),
    ).toBeInTheDocument();
  });
});
