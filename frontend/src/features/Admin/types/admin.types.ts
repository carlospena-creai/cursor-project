/**
 * Admin Feature - Type Definitions
 *
 * Define los tipos de datos para el feature de administración.
 */

export interface DashboardStats {
  total_products: number;
  active_products: number;
  total_orders: number;
  pending_orders: number;
  total_users: number;
  active_users: number;
  total_revenue: number;
  recent_orders_count: number;
}

export interface ProductBulkCreate {
  products: Array<{
    name: string;
    description?: string;
    price: number;
    stock: number;
    category?: string;
  }>;
}

export interface ProductBulkUpdate {
  updates: Array<{
    product_id: number;
    name?: string;
    description?: string;
    price?: number;
    stock?: number;
    category?: string;
    is_active?: boolean;
  }>;
}

export interface ProductBulkDelete {
  product_ids: number[];
}

// Users Management Types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  is_active: boolean;
  is_admin: boolean;
  created_at: string | null;
}

export interface UsersResponse {
  users: User[];
  total: number;
  limit: number;
  offset: number;
}

export interface UsersFilters {
  is_active?: boolean | null;
  is_admin?: boolean | null;
  search?: string;
  limit?: number;
  offset?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}

export interface UserUpdate {
  email?: string;
  username?: string;
  full_name?: string | null;
  is_active?: boolean;
  is_admin?: boolean;
}
