import { render, screen, waitFor } from '@testing-library/react';
import TaskFormModal from '../../components/TaskFormModal';
import { vi, describe, beforeEach, it, expect } from 'vitest';
import userEvent from '@testing-library/user-event';

describe('TaskFormModal', () => {
  const mockOnClose = vi.fn();
  const mockOnSubmit = vi.fn().mockResolvedValue(undefined);

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza o modal com título padrão e formulário', () => {
    render(
      <TaskFormModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />,
    );

    expect(screen.getByText('Nova Tarefa')).toBeInTheDocument();
    expect(screen.getByLabelText(/título/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/descrição/i)).toBeInTheDocument();
  });

  it('mostra título "Editar Tarefa" se editMode for true', () => {
    render(
      <TaskFormModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        editMode
      />,
    );

    expect(screen.getByText('Editar Tarefa')).toBeInTheDocument();
  });

  it('submete dados válidos do formulário e fecha o modal', async () => {
    render(
      <TaskFormModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />,
    );

    await userEvent.type(screen.getByLabelText(/título/i), 'Minha tarefa');
    await userEvent.type(
      screen.getByLabelText(/descrição/i),
      'Descrição da tarefa',
    );
    await userEvent.click(screen.getByRole('button', { name: /salvar/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'Minha tarefa',
        description: 'Descrição da tarefa',
      });
    });
  });

  it('chama onClose ao clicar em "Cancelar"', async () => {
    render(
      <TaskFormModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />,
    );

    await userEvent.click(screen.getByRole('button', { name: /cancelar/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });
});
