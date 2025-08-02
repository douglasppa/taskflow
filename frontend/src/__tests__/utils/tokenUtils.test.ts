import { describe, it, expect, vi, beforeEach } from 'vitest';
import { decodeToken, getToken } from '../../utils/tokenUtils';
import type { JwtPayload } from '../../utils/tokenUtils';
import { jwtDecode } from 'jwt-decode';
import type { Mock } from 'vitest';

// mock do jwt-decode
vi.mock('jwt-decode', () => ({
  jwtDecode: vi.fn(),
}));

describe('tokenUtils', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('decodeToken deve chamar jwtDecode com o token correto', () => {
    const token = 'meu.token.fake';
    const payload: JwtPayload = {
      sub: '123',
      email: 'teste@example.com',
      exp: 99999999,
    };

    (jwtDecode as unknown as Mock).mockReturnValue(payload);

    const result = decodeToken(token);

    expect(jwtDecode).toHaveBeenCalledWith(token);
    expect(result).toEqual(payload);
  });

  it('getToken deve retornar o token armazenado no localStorage', () => {
    localStorage.setItem('token', 'token123');
    expect(getToken()).toBe('token123');
  });

  it('getToken deve retornar null se não houver token no localStorage', () => {
    expect(getToken()).toBeNull();
  });
});
