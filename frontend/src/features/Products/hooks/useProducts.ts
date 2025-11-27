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
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  setFilters: (filters: ProductsFilters) => void;
}

export function useProducts(
  initialFilters?: ProductsFilters
): UseProductsReturn {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ProductsFilters>(initialFilters || {});

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productsApi.getProducts(filters);
      setProducts(data);
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
    loading,
    error,
    refetch: fetchProducts,
    setFilters,
  };
}
