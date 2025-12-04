/**
 * Users Admin API Service
 *
 * Maneja todas las llamadas HTTP al backend de administración de usuarios.
 */
import apiClient from "@shared/services/apiClient";
import type {
  UsersResponse,
  UsersFilters,
  User,
  UserUpdate,
} from "../types/admin.types";

const API_BASE_URL = "http://localhost:8000";

class UsersAdminApiService {
  /**
   * Obtiene todos los usuarios con filtros opcionales
   */
  async getUsers(filters: UsersFilters = {}): Promise<UsersResponse> {
    try {
      const params = new URLSearchParams();

      if (filters.is_active !== undefined && filters.is_active !== null) {
        params.append("is_active", filters.is_active.toString());
      }
      if (filters.is_admin !== undefined && filters.is_admin !== null) {
        params.append("is_admin", filters.is_admin.toString());
      }
      if (filters.search) {
        params.append("search", filters.search);
      }
      if (filters.limit) {
        params.append("limit", filters.limit.toString());
      }
      if (filters.offset) {
        params.append("offset", filters.offset.toString());
      }
      if (filters.sort_by) {
        params.append("sort_by", filters.sort_by);
      }
      if (filters.sort_order) {
        params.append("sort_order", filters.sort_order);
      }

      const queryString = params.toString();
      const url = `${API_BASE_URL}/admin/users${
        queryString ? `?${queryString}` : ""
      }`;

      return await apiClient.get<UsersResponse>(url);
    } catch (error) {
      console.error("Error in getUsers:", error);
      throw error;
    }
  }

  /**
   * Actualiza un usuario existente
   */
  async updateUser(userId: number, data: UserUpdate): Promise<User> {
    try {
      return await apiClient.put<User>(
        `${API_BASE_URL}/admin/users/${userId}`,
        data
      );
    } catch (error) {
      console.error("Error in updateUser:", error);
      throw error;
    }
  }
}

// Exportar instancia singleton
export const usersAdminApi = new UsersAdminApiService();
