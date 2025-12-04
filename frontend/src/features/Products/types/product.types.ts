/**
 * Products Feature - Type Definitions
 *
 * Define los tipos de datos para el feature de productos.
 */

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
  category: string;
  description: string | null;
  is_active: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface ProductsFilters {
  category?: string;
  min_price?: number;
  max_price?: number;
  search?: string;
  limit?: number;
  offset?: number;
  only_active?: boolean;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}

export interface ProductsResponse {
  products: Product[];
  total: number;
  limit: number;
  offset: number;
}
