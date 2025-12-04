/**
 * Admin Feature - Public Exports
 *
 * Exporta todos los componentes, hooks y utilidades del feature de administración.
 */

// Pages
export { default as DashboardPage } from "./pages/DashboardPage";

// Components
export { AdminRoute } from "./components/AdminRoute";
export { StatsCard } from "./components/StatsCard";

// Hooks
export { useDashboardStats } from "./hooks/useDashboardStats";

// Types
export type { DashboardStats } from "./types/admin.types";

// Utils
export { adminApi } from "./utils/adminApi";
