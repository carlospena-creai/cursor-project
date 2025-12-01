/**
 * useCreateOrder Hook
 *
 * Custom hook para crear órdenes.
 * Maneja loading, error states y success callbacks.
 */
import { useState, useCallback } from "react";
import { ordersApi } from "../utils/ordersApi";
import type { Order, OrderCreate } from "../types/order.types";

interface UseCreateOrderReturn {
  createOrder: (orderData: OrderCreate) => Promise<Order | null>;
  loading: boolean;
  error: string | null;
}

export function useCreateOrder(): UseCreateOrderReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createOrder = useCallback(
    async (orderData: OrderCreate): Promise<Order | null> => {
      try {
        setLoading(true);
        setError(null);
        const order = await ordersApi.createOrder(orderData);
        return order;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error creating order";
        setError(errorMessage);
        console.error("Error creating order:", err);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    createOrder,
    loading,
    error,
  };
}

