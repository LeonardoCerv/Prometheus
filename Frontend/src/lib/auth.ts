// auth.ts - JWT authentication utilities

const JWT_TOKEN_KEY = 'prometheus_jwt_token';

export interface JWTPayload {
  userId: string;
  email: string;
  exp: number;
  // Add other fields as needed
}

export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(JWT_TOKEN_KEY);
};

export const setToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(JWT_TOKEN_KEY, token);
};

export const removeToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(JWT_TOKEN_KEY);
};

export const decodeToken = (token: string): JWTPayload | null => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

export const getCurrentUser = (): JWTPayload | null => {
  const token = getToken();
  if (!token) return null;
  return decodeToken(token);
};

export const isTokenExpired = (token: string): boolean => {
  const payload = decodeToken(token);
  if (!payload) return true;
  return payload.exp * 1000 < Date.now();
};

export const isAuthenticated = (): boolean => {
  const token = getToken();
  if (!token) return false;
  return !isTokenExpired(token);
};
