/**
 * useOrders Hook
 *
 * Custom hook para manejar el estado y lógica de órdenes.
 * Encapsula fetching, loading states, error handling.
 */
import { useState, useEffect, useCallback } from "react";
import { ordersApi } from "../utils/ordersApi";
import type { Order, OrdersFilters } from "../types/order.types";

interface UseOrdersReturn {
  orders: Order[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useOrders(filters?: OrdersFilters): UseOrdersReturn {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ordersApi.getOrders(filters);
      setOrders(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error loading orders");
      console.error("Error fetching orders:", err);
    } finally {
      setLoading(false);
    }
  }, [filters?.user_id, filters?.status, filters?.limit, filters?.offset]);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  return {
    orders,
    loading,
    error,
    refetch: fetchOrders,
  };
}
