/**
 * Orders API Service
 *
 * Maneja todas las llamadas HTTP al backend de órdenes.
 * Encapsula la lógica de API en un solo lugar.
 */
import apiClient from "@shared/services/apiClient";
import type {
  Order,
  OrderCreate,
  OrderUpdate,
  OrdersFilters,
  OrdersResponse,
  OrderStatus,
} from "../types/order.types";

const API_BASE_URL = "http://localhost:8000";

class OrdersApiService {
  /**
   * Obtiene la lista de órdenes con filtros opcionales
   * Retorna órdenes paginadas con total
   */
  async getOrders(filters?: OrdersFilters): Promise<OrdersResponse> {
    try {
      const params = new URLSearchParams();

      if (filters?.status) params.append("status", filters.status);
      if (filters?.limit) params.append("limit", filters.limit.toString());
      if (filters?.offset) params.append("offset", filters.offset.toString());
      if (filters?.sort_by) params.append("sort_by", filters.sort_by);
      if (filters?.sort_order) params.append("sort_order", filters.sort_order);

      const queryString = params.toString();
      const url = `/orders${queryString ? `?${queryString}` : ""}`;

      return await apiClient.get<OrdersResponse>(url);
    } catch (error) {
      console.error("Error in getOrders:", error);
      throw error;
    }
  }

  /**
   * Obtiene una orden por ID
   */
  async getOrderById(id: number): Promise<Order> {
    try {
      return await apiClient.get<Order>(`/orders/${id}`);
    } catch (error) {
      console.error(`Error in getOrderById(${id}):`, error);
      throw error;
    }
  }

  /**
   * Crea una nueva orden
   */
  async createOrder(orderData: OrderCreate): Promise<Order> {
    try {
      return await apiClient.post<Order>("/orders", orderData);
    } catch (error) {
      console.error("Error in createOrder:", error);
      throw error;
    }
  }

  /**
   * Actualiza el estado de una orden
   */
  async updateOrderStatus(
    orderId: number,
    status: OrderStatus
  ): Promise<Order> {
    try {
      const token = localStorage.getItem("auth_token");
      const headers: HeadersInit = {
        "Content-Type": "application/json",
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/orders/${orderId}/status`, {
        method: "PATCH",
        headers,
        body: JSON.stringify({ status }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error updating order status");
      }

      return await response.json();
    } catch (error) {
      console.error(`Error in updateOrderStatus(${orderId}):`, error);
      throw error;
    }
  }

  /**
   * Actualiza una orden
   */
  async updateOrder(orderId: number, orderData: OrderUpdate): Promise<Order> {
    try {
      return await apiClient.put<Order>(`/orders/${orderId}`, orderData);
    } catch (error) {
      console.error(`Error in updateOrder(${orderId}):`, error);
      throw error;
    }
  }
}

// Exportar instancia singleton
export const ordersApi = new OrdersApiService();
