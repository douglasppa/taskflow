import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import * as taskService from '../../services/taskService';

// Mocks
vi.mock('axios');
vi.mock('../../utils/tokenUtils', () => ({
  getToken: () => 'mock-token',
}));

const mockedAxios = axios as unknown as {
  get: ReturnType<typeof vi.fn>;
  post: ReturnType<typeof vi.fn>;
  put: ReturnType<typeof vi.fn>;
  delete: ReturnType<typeof vi.fn>;
};

describe('taskService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve buscar tarefas com token no header', async () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Tarefa 1',
        description: 'Descrição 1',
        status: 'pending',
      },
    ];
    mockedAxios.get = vi.fn().mockResolvedValue({ data: mockTasks });

    const result = await taskService.getTasks();

    expect(mockedAxios.get).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/tasks?skip=0&limit=10'),
      expect.objectContaining({
        headers: { Authorization: 'Bearer mock-token' },
      }),
    );
    expect(result).toEqual(mockTasks);
  });

  it('deve criar uma nova tarefa', async () => {
    mockedAxios.post = vi.fn().mockResolvedValue({});

    await taskService.createTask({ title: 'Nova', description: 'Descrição' });

    expect(mockedAxios.post).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/tasks'),
      { title: 'Nova', description: 'Descrição' },
      expect.objectContaining({
        headers: { Authorization: 'Bearer mock-token' },
      }),
    );
  });

  it('deve atualizar uma tarefa existente', async () => {
    mockedAxios.put = vi.fn().mockResolvedValue({});

    await taskService.updateTask(42, {
      title: 'Atualizada',
      description: 'Nova desc',
    });

    expect(mockedAxios.put).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/tasks/42'),
      { title: 'Atualizada', description: 'Nova desc' },
      expect.objectContaining({
        headers: { Authorization: 'Bearer mock-token' },
      }),
    );
  });

  it('deve excluir uma tarefa', async () => {
    mockedAxios.delete = vi.fn().mockResolvedValue({});

    await taskService.deleteTask(99);

    expect(mockedAxios.delete).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/tasks/99'),
      expect.objectContaining({
        headers: { Authorization: 'Bearer mock-token' },
      }),
    );
  });
});
