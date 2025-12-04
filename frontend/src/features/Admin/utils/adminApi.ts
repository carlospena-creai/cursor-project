/**
 * Admin API Service
 *
 * Maneja todas las llamadas HTTP al backend de administración.
 */
import apiClient from "@shared/services/apiClient";
import type {
  DashboardStats,
  ProductBulkCreate,
  ProductBulkUpdate,
  ProductBulkDelete,
} from "../types/admin.types";
import type { Product } from "../../Products/types/product.types";

class AdminApiService {
  /**
   * Obtiene las estadísticas del dashboard
   */
  async getDashboardStats(): Promise<DashboardStats> {
    try {
      return await apiClient.get<DashboardStats>("/admin/dashboard/stats");
    } catch (error) {
      console.error("Error in getDashboardStats:", error);
      throw error;
    }
  }

  /**
   * Crea múltiples productos en una sola operación
   */
  async bulkCreateProducts(bulkData: ProductBulkCreate): Promise<Product[]> {
    try {
      return await apiClient.post<Product[]>(
        "/admin/products/bulk-create",
        bulkData
      );
    } catch (error) {
      console.error("Error in bulkCreateProducts:", error);
      throw error;
    }
  }

  /**
   * Actualiza múltiples productos en una sola operación
   */
  async bulkUpdateProducts(bulkData: ProductBulkUpdate): Promise<Product[]> {
    try {
      return await apiClient.put<Product[]>(
        "/admin/products/bulk-update",
        bulkData
      );
    } catch (error) {
      console.error("Error in bulkUpdateProducts:", error);
      throw error;
    }
  }

  /**
   * Elimina múltiples productos en una sola operación
   */
  async bulkDeleteProducts(bulkData: ProductBulkDelete): Promise<void> {
    try {
      // Usar fetch directamente para DELETE con body
      const token = localStorage.getItem("auth_token");
      const headers: HeadersInit = {
        "Content-Type": "application/json",
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      const response = await fetch(
        "http://localhost:8000/admin/products/bulk-delete",
        {
          method: "DELETE",
          headers,
          body: JSON.stringify(bulkData),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error deleting products");
      }
    } catch (error) {
      console.error("Error in bulkDeleteProducts:", error);
      throw error;
    }
  }
}

// Exportar instancia singleton
export const adminApi = new AdminApiService();
