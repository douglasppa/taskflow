// src/utils/tokenUtils.ts

import { jwtDecode } from 'jwt-decode';

export interface JwtPayload {
  sub: string;
  email: string;
  exp: number;
}

export function decodeToken(token: string) {
  return jwtDecode<JwtPayload>(token);
}