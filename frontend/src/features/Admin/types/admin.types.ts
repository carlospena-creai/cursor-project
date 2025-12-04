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
