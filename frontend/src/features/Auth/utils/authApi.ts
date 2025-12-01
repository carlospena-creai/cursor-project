/**
 * Auth API Service
 *
 * Maneja todas las llamadas HTTP al backend de autenticación.
 */
import apiClient from "@shared/services/apiClient";
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
} from "../types/auth.types";

const API_BASE_URL = "http://localhost:8000";

class AuthApiService {
  /**
   * Registra un nuevo usuario
   */
  async register(data: RegisterRequest): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error registering user");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in register:", error);
      throw error;
    }
  }

  /**
   * Autentica un usuario y obtiene token
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error during login");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in login:", error);
      throw error;
    }
  }

  /**
   * Obtiene el perfil del usuario autenticado
   */
  async getProfile(): Promise<User> {
    try {
      return await apiClient.get<User>("/auth/profile");
    } catch (error) {
      console.error("Error in getProfile:", error);
      throw error;
    }
  }
}

// Exportar instancia singleton
export const authApi = new AuthApiService();
