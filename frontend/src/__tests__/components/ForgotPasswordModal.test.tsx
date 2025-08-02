import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ForgotPasswordModal from '../../components/ForgotPasswordModal';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
  },
}));

const mockedAxios = axios as unknown as {
  post: ReturnType<typeof vi.fn>;
};

describe('ForgotPasswordModal', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('não renderiza se isOpen for false', () => {
    const { container } = render(
      <ForgotPasswordModal isOpen={false} onClose={mockOnClose} />,
    );
    expect(container.firstChild).toBeNull();
  });

  it('renderiza corretamente quando isOpen for true', () => {
    render(<ForgotPasswordModal isOpen={true} onClose={mockOnClose} />);
    expect(screen.getByText('Recuperar acesso')).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText('Digite seu e-mail'),
    ).toBeInTheDocument();
  });

  it('envia corretamente e mostra mensagem de sucesso', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: { message: 'E-mail enviado!' },
    });

    render(<ForgotPasswordModal isOpen={true} onClose={mockOnClose} />);

    fireEvent.change(screen.getByPlaceholderText('Digite seu e-mail'), {
      target: { value: 'teste@exemplo.com' },
    });

    fireEvent.click(screen.getByRole('button', { name: /enviar instruções/i }));

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalled();
      expect(screen.getByText(/e-mail enviado!/i)).toBeInTheDocument();
    });
  });

  it('fecha e reseta ao clicar no ✕', () => {
    render(<ForgotPasswordModal isOpen={true} onClose={mockOnClose} />);
    fireEvent.click(screen.getByRole('button', { name: /✕/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });
});
