/**
 * Orders Feature - Public Exports
 *
 * Exporta todos los componentes, hooks y utilidades del feature de órdenes.
 */

// Pages
export { default as CartPage } from "./pages/CartPage";
export { default as CheckoutPage } from "./pages/CheckoutPage";
export { default as OrdersPage } from "./pages/OrdersPage";

// Components
export { CartItem } from "./components/CartItem";
export { CartSummary } from "./components/CartSummary";
export { OrderCard } from "./components/OrderCard";
export { OrderList } from "./components/OrderList";

// Context
export { CartProvider, useCart } from "./context/CartContext";

// Hooks
export { useOrders } from "./hooks/useOrders";
export { useCreateOrder } from "./hooks/useCreateOrder";

// Types
export type {
  Order,
  OrderItem,
  OrderItemCreate,
  OrderCreate,
  OrderUpdate,
  OrderStatus,
  OrdersFilters,
  CartItem as CartItemType,
} from "./types/order.types";

// Utils
export { ordersApi } from "./utils/ordersApi";
