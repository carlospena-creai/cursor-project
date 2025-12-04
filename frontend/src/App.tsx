import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CartProvider } from "./features/Orders/context/CartContext";
import { AuthProvider, ProtectedRoute } from "./features/Auth";
import { AdminRoute, AdminLayout } from "./features/Admin";
import MainLayout from "@shared/components/Layout/MainLayout";
import { ErrorBoundary } from "@shared/components/ErrorBoundary";
import LoadingFallback from "@shared/components/LoadingFallback";

// ✅ Lazy loading de rutas para mejor performance
const ProductsPage = lazy(() =>
  import("./features/Products").then((module) => ({
    default: module.ProductsPage,
  }))
);
const SearchResultsPage = lazy(
  () => import("./features/Products/pages/SearchResultsPage")
);
const CartPage = lazy(() =>
  import("./features/Orders").then((module) => ({ default: module.CartPage }))
);
const CheckoutPage = lazy(() =>
  import("./features/Orders").then((module) => ({
    default: module.CheckoutPage,
  }))
);
const OrdersPage = lazy(() =>
  import("./features/Orders").then((module) => ({ default: module.OrdersPage }))
);
const LoginPage = lazy(() =>
  import("./features/Auth").then((module) => ({ default: module.LoginPage }))
);
const RegisterPage = lazy(() =>
  import("./features/Auth").then((module) => ({ default: module.RegisterPage }))
);
const ProfilePage = lazy(() =>
  import("./features/Auth").then((module) => ({ default: module.ProfilePage }))
);
const DashboardPage = lazy(() =>
  import("./features/Admin").then((module) => ({
    default: module.DashboardPage,
  }))
);
const ProductsManagementPage = lazy(() =>
  import("./features/Admin").then((module) => ({
    default: module.ProductsManagementPage,
  }))
);
const OrdersManagementPage = lazy(() =>
  import("./features/Admin").then((module) => ({
    default: module.OrdersManagementPage,
  }))
);
const UsersManagementPage = lazy(() =>
  import("./features/Admin").then((module) => ({
    default: module.UsersManagementPage,
  }))
);
const NotFoundPage = lazy(() => import("./shared/pages/NotFoundPage"));

// ✅ Error boundaries implementados para manejar crashes
// ✅ Loading states globales con Suspense
// ❌ PROBLEMA: No configuración de rutas protegidas
// ✅ Lazy loading de rutas implementado
// ✅ Página 404 y catch-all route implementados
// ❌ PROBLEMA: No configuración de SEO (meta tags, etc.)

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <CartProvider>
            <Suspense fallback={<LoadingFallback />}>
              <Routes>
                {/* Rutas con MainLayout (header y footer) */}
                <Route
                  path="/"
                  element={
                    <MainLayout>
                      <ProductsPage />
                    </MainLayout>
                  }
                />
                <Route
                  path="/search"
                  element={
                    <MainLayout>
                      <SearchResultsPage />
                    </MainLayout>
                  }
                />
                <Route
                  path="/login"
                  element={
                    <MainLayout>
                      <LoginPage />
                    </MainLayout>
                  }
                />
                <Route
                  path="/register"
                  element={
                    <MainLayout>
                      <RegisterPage />
                    </MainLayout>
                  }
                />
                <Route
                  path="/cart"
                  element={
                    <ProtectedRoute>
                      <MainLayout>
                        <CartPage />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/checkout"
                  element={
                    <ProtectedRoute>
                      <MainLayout>
                        <CheckoutPage />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/orders"
                  element={
                    <ProtectedRoute>
                      <MainLayout>
                        <OrdersPage />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <MainLayout>
                        <ProfilePage />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />

                {/* Rutas de Admin con AdminLayout (sin header principal) */}
                <Route
                  path="/admin"
                  element={
                    <AdminRoute>
                      <AdminLayout>
                        <DashboardPage />
                      </AdminLayout>
                    </AdminRoute>
                  }
                />
                <Route
                  path="/admin/products"
                  element={
                    <AdminRoute>
                      <AdminLayout>
                        <ProductsManagementPage />
                      </AdminLayout>
                    </AdminRoute>
                  }
                />
                <Route
                  path="/admin/orders"
                  element={
                    <AdminRoute>
                      <AdminLayout>
                        <OrdersManagementPage />
                      </AdminLayout>
                    </AdminRoute>
                  }
                />
                <Route
                  path="/admin/users"
                  element={
                    <AdminRoute>
                      <AdminLayout>
                        <UsersManagementPage />
                      </AdminLayout>
                    </AdminRoute>
                  }
                />
                {/* ❌ PROBLEMA: More routes will be added but no route protection */}
                {/* TODO Day 2: /products, /products/:id */}

                {/* ✅ Página 404 y catch-all route */}
                <Route
                  path="*"
                  element={
                    <MainLayout>
                      <NotFoundPage />
                    </MainLayout>
                  }
                />
              </Routes>
            </Suspense>
          </CartProvider>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  );
};

export default App;
