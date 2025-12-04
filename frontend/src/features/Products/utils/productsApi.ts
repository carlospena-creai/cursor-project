/**
 * Products API Service
 *
 * Maneja todas las llamadas HTTP al backend de productos.
 * Encapsula la lógica de API en un solo lugar.
 */
import type {
  Product,
  ProductsFilters,
  ProductsResponse,
} from "../types/product.types";

const API_BASE_URL = "http://localhost:8000";

class ProductsApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Obtiene la lista de productos con filtros opcionales
   * Retorna productos paginados con total
   */
  async getProducts(filters?: ProductsFilters): Promise<ProductsResponse> {
    try {
      const params = new URLSearchParams();

      if (filters?.category) params.append("category", filters.category);
      if (filters?.min_price !== undefined)
        params.append("min_price", filters.min_price.toString());
      if (filters?.max_price !== undefined)
        params.append("max_price", filters.max_price.toString());
      if (filters?.search) params.append("search", filters.search);
      if (filters?.limit) params.append("limit", filters.limit.toString());
      if (filters?.offset) params.append("offset", filters.offset.toString());
      if (filters?.only_active !== undefined)
        params.append("only_active", filters.only_active.toString());

      const url = `${this.baseUrl}/products?${params.toString()}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Error fetching products: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Error in getProducts:", error);
      throw error;
    }
  }

  /**
   * Obtiene un producto por ID
   */
  async getProductById(id: number): Promise<Product> {
    try {
      const response = await fetch(`${this.baseUrl}/products/${id}`);

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Product not found");
        }
        throw new Error(`Error fetching product: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error in getProductById(${id}):`, error);
      throw error;
    }
  }

  /**
   * Crea un nuevo producto
   */
  async createProduct(
    productData: Omit<Product, "id" | "created_at" | "updated_at">
  ): Promise<Product> {
    try {
      const response = await fetch(`${this.baseUrl}/products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(productData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error creating product");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in createProduct:", error);
      throw error;
    }
  }

  /**
   * Actualiza un producto existente
   */
  async updateProduct(
    id: number,
    productData: Partial<Product>
  ): Promise<Product> {
    try {
      const response = await fetch(`${this.baseUrl}/products/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(productData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error updating product");
      }

      return await response.json();
    } catch (error) {
      console.error(`Error in updateProduct(${id}):`, error);
      throw error;
    }
  }

  /**
   * Elimina un producto (soft delete)
   */
  async deleteProduct(id: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/products/${id}`, {
        method: "DELETE",
      });

      if (!response.ok && response.status !== 204) {
        const error = await response.json();
        throw new Error(error.detail || "Error deleting product");
      }
    } catch (error) {
      console.error(`Error in deleteProduct(${id}):`, error);
      throw error;
    }
  }
}

// Exportar instancia singleton
export const productsApi = new ProductsApiService();
