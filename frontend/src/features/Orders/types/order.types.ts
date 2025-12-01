/**
 * Orders Feature - Type Definitions
 *
 * Define los tipos de datos para el feature de órdenes y carrito.
 */

export type OrderStatus =
  | "pending"
  | "confirmed"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled";

export interface OrderItem {
  id?: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface OrderItemCreate {
  product_id: number;
  quantity: number;
}

export interface Order {
  id?: number;
  user_id: number;
  items: OrderItem[];
  status: OrderStatus;
  total: number;
  shipping_address?: string | null;
  notes?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface OrderCreate {
  user_id: number;
  items: OrderItemCreate[];
  shipping_address?: string;
  notes?: string;
}

export interface OrderUpdate {
  status?: OrderStatus;
  shipping_address?: string;
  notes?: string;
}

export interface OrdersFilters {
  user_id?: number;
  status?: OrderStatus;
  limit?: number;
  offset?: number;
}

export interface CartItem {
  productId: number;
  productName: string;
  quantity: number;
  unitPrice: number;
  subtotal: number;
}
