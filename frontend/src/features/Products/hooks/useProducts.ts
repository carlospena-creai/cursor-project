/**
 * useProducts Hook
 *
 * Custom hook para manejar el estado y lógica de productos.
 * Encapsula fetching, loading states, error handling.
 */
import { useState, useEffect, useCallback } from "react";
import { productsApi } from "../utils/productsApi";
import type { Product, ProductsFilters } from "../types/product.types";

interface UseProductsReturn {
  products: Product[];
  total: number;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useProducts(filters?: ProductsFilters): UseProductsReturn {
  const [products, setProducts] = useState<Product[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productsApi.getProducts(filters);
      setProducts(data.products);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error loading products");
      console.error("Error fetching products:", err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  return {
    products,
    total,
    loading,
    error,
    refetch: fetchProducts,
  };
}
