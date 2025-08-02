import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TaskForm from '../../components/TaskForm';
import type { TaskFormData } from '../../components/TaskForm';

describe('TaskForm', () => {
  const mockOnSubmit = vi.fn();
  const mockOnCancel = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('exibe erros de validação se os campos estiverem vazios', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    fireEvent.click(screen.getByRole('button', { name: /salvar/i }));

    expect(await screen.findByText(/título obrigatório/i)).toBeInTheDocument();
    expect(
      await screen.findByText(/descrição obrigatória/i),
    ).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('chama onSubmit com dados válidos', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    fireEvent.input(screen.getByLabelText(/título/i), {
      target: { value: 'Título de teste' },
    });

    fireEvent.input(screen.getByLabelText(/descrição/i), {
      target: { value: 'Descrição de teste' },
    });

    fireEvent.click(screen.getByRole('button', { name: /salvar/i }));

    await waitFor(() => {
      expect(mockOnSubmit.mock.calls[0][0]).toEqual({
        title: 'Título de teste',
        description: 'Descrição de teste',
      });
    });
  });

  it('exibe os valores iniciais quando fornecidos', () => {
    const initialData: TaskFormData = {
      title: 'Título inicial',
      description: 'Descrição inicial',
    };

    render(<TaskForm onSubmit={mockOnSubmit} initialData={initialData} />);

    expect(screen.getByDisplayValue(/título inicial/i)).toBeInTheDocument();
    expect(screen.getByDisplayValue(/descrição inicial/i)).toBeInTheDocument();
  });

  it('chama onCancel ao clicar no botão "Cancelar"', () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    fireEvent.click(screen.getByRole('button', { name: /cancelar/i }));

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('exibe indicador de loading quando isSubmitting for true', () => {
    render(<TaskForm onSubmit={mockOnSubmit} isSubmitting />);

    expect(screen.getByText(/salvando/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /salvando/i })).toBeDisabled();
  });
});
