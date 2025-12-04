/**
 * Admin Feature - Public Exports
 *
 * Exporta todos los componentes, hooks y utilidades del feature de administración.
 */

// Pages
export { default as DashboardPage } from "./pages/DashboardPage";
export { default as ProductsManagementPage } from "./pages/ProductsManagementPage";
export { default as OrdersManagementPage } from "./pages/OrdersManagementPage";
export { default as UsersManagementPage } from "./pages/UsersManagementPage";

// Components
export { AdminRoute } from "./components/AdminRoute";
export { StatsCard } from "./components/StatsCard";
export { ProductFormModal } from "./components/ProductFormModal";
export { default as AdminLayout } from "./components/AdminLayout";

// Hooks
export { useDashboardStats } from "./hooks/useDashboardStats";
export { useProductsManagement } from "./hooks/useProductsManagement";
export { useOrdersManagement } from "./hooks/useOrdersManagement";
export { useUsersManagement } from "./hooks/useUsersManagement";
export { useUsers } from "./hooks/useUsers";

// Types
export type { DashboardStats } from "./types/admin.types";

// Utils
export { adminApi } from "./utils/adminApi";
