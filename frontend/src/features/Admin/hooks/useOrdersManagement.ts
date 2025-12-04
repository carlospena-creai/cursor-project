/**
 * Hook para gestión de órdenes en el admin panel
 *
 * Maneja actualización de estado de órdenes
 */
import { useState, useCallback } from "react";
import { message } from "antd";
import { ordersApi } from "../../Orders/utils/ordersApi";
import type { Order, OrderStatus } from "../../Orders/types/order.types";

interface UseOrdersManagementReturn {
  loading: boolean;
  error: string | null;
  updateOrderStatus: (
    orderId: number,
    newStatus: OrderStatus
  ) => Promise<Order | null>;
}

export function useOrdersManagement(): UseOrdersManagementReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const updateOrderStatus = useCallback(
    async (orderId: number, newStatus: OrderStatus): Promise<Order | null> => {
      try {
        setLoading(true);
        setError(null);

        const order = await ordersApi.updateOrderStatus(orderId, newStatus);

        message.success("Estado de orden actualizado exitosamente");
        return order;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error updating order status";
        setError(errorMessage);
        message.error(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    loading,
    error,
    updateOrderStatus,
  };
}

