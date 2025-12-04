import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ProductsPage } from "./features/Products";
import SearchResultsPage from "./features/Products/pages/SearchResultsPage";
import { CartProvider } from "./features/Orders/context/CartContext";
import { CartPage, CheckoutPage, OrdersPage } from "./features/Orders";
import {
  AuthProvider,
  LoginPage,
  RegisterPage,
  ProfilePage,
  ProtectedRoute,
} from "./features/Auth";
import {
  DashboardPage,
  ProductsManagementPage,
  OrdersManagementPage,
  AdminRoute,
  AdminLayout,
} from "./features/Admin";
import MainLayout from "@shared/components/Layout/MainLayout";

// ❌ PROBLEMA: No error boundaries para manejar crashes
// ❌ PROBLEMA: No loading states globales
// ❌ PROBLEMA: No configuración de rutas protegidas
// ❌ PROBLEMA: No lazy loading de rutas
// ❌ PROBLEMA: No configuración de SEO (meta tags, etc.)
const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <CartProvider>
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
            {/* ❌ PROBLEMA: More routes will be added but no route protection */}
            {/* TODO Day 2: /products, /products/:id */}

            {/* ❌ PROBLEMA: No 404 route */}
            {/* ❌ PROBLEMA: No catch-all route */}
          </Routes>
        </CartProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
