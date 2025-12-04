/**
 * Hook para gestión de productos en el admin panel
 *
 * Maneja todas las operaciones CRUD y bulk operations
 */
import { useState, useCallback } from "react";
import { message } from "antd";
import { adminApi } from "../utils/adminApi";
import type { Product } from "../../Products/types/product.types";
import type {
  ProductBulkCreate,
  ProductBulkUpdate,
  ProductBulkDelete,
} from "../types/admin.types";

interface UseProductsManagementReturn {
  loading: boolean;
  error: string | null;
  createProduct: (
    productData: Omit<Product, "id" | "created_at" | "updated_at">
  ) => Promise<Product | null>;
  updateProduct: (
    id: number,
    productData: Partial<Product>
  ) => Promise<Product | null>;
  deleteProduct: (id: number) => Promise<boolean>;
  bulkCreate: (data: ProductBulkCreate) => Promise<Product[] | null>;
  bulkUpdate: (data: ProductBulkUpdate) => Promise<Product[] | null>;
  bulkDelete: (data: ProductBulkDelete) => Promise<boolean>;
}

export function useProductsManagement(): UseProductsManagementReturn {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const createProduct = useCallback(
    async (
      productData: Omit<Product, "id" | "created_at" | "updated_at">
    ): Promise<Product | null> => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("auth_token");
        if (!token) {
          throw new Error("No authentication token found");
        }

        const response = await fetch("http://localhost:8000/products", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(productData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Error creating product");
        }

        const product = await response.json();
        message.success("Producto creado exitosamente");
        return product;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error creating product";
        setError(errorMessage);
        message.error(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const updateProduct = useCallback(
    async (
      id: number,
      productData: Partial<Product>
    ): Promise<Product | null> => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("auth_token");
        if (!token) {
          throw new Error("No authentication token found");
        }

        const response = await fetch(`http://localhost:8000/products/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(productData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Error updating product");
        }

        const product = await response.json();
        message.success("Producto actualizado exitosamente");
        return product;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error updating product";
        setError(errorMessage);
        message.error(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const deleteProduct = useCallback(async (id: number): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("auth_token");
      if (!token) {
        throw new Error("No authentication token found");
      }

      const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok && response.status !== 204) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error deleting product");
      }

      message.success("Producto eliminado exitosamente");
      return true;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Error deleting product";
      setError(errorMessage);
      message.error(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const bulkCreate = useCallback(
    async (data: ProductBulkCreate): Promise<Product[] | null> => {
      try {
        setLoading(true);
        setError(null);
        const products = await adminApi.bulkCreateProducts(data);
        message.success(
          `${products.length} producto(s) creado(s) exitosamente`
        );
        return products;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error creating products";
        setError(errorMessage);
        message.error(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const bulkUpdate = useCallback(
    async (data: ProductBulkUpdate): Promise<Product[] | null> => {
      try {
        setLoading(true);
        setError(null);
        const products = await adminApi.bulkUpdateProducts(data);
        message.success(
          `${products.length} producto(s) actualizado(s) exitosamente`
        );
        return products;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error updating products";
        setError(errorMessage);
        message.error(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const bulkDelete = useCallback(
    async (data: ProductBulkDelete): Promise<boolean> => {
      try {
        setLoading(true);
        setError(null);
        await adminApi.bulkDeleteProducts(data);
        message.success(
          `${data.product_ids.length} producto(s) eliminado(s) exitosamente`
        );
        return true;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Error deleting products";
        setError(errorMessage);
        message.error(errorMessage);
        return false;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    loading,
    error,
    createProduct,
    updateProduct,
    deleteProduct,
    bulkCreate,
    bulkUpdate,
    bulkDelete,
  };
}
