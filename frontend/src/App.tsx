import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Layout } from "antd";
import AppHeader from "@shared/components/Layout/Header";
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

const { Content, Footer } = Layout;

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
          {/* ❌ PROBLEMA: Layout muy básico sin responsiveness avanzada */}
          <Layout style={{ minHeight: "100vh" }}>
            <AppHeader />

            {/* ❌ PROBLEMA: Content padding hardcodeado sin responsiveness */}
            <Content style={{ padding: "24px 50px" }}>
              {/* ❌ PROBLEMA: No error boundary wrapper para rutas */}
              {/* ❌ PROBLEMA: No loading fallback para suspense */}
              <Routes>
                <Route path="/" element={<ProductsPage />} />
                <Route path="/search" element={<SearchResultsPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route
                  path="/cart"
                  element={
                    <ProtectedRoute>
                      <CartPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/checkout"
                  element={
                    <ProtectedRoute>
                      <CheckoutPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/orders"
                  element={
                    <ProtectedRoute>
                      <OrdersPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <ProfilePage />
                    </ProtectedRoute>
                  }
                />
                {/* ❌ PROBLEMA: More routes will be added but no route protection */}
                {/* TODO Day 2: /products, /products/:id */}
                {/* TODO Day 5: /admin/* (protected routes) */}

                {/* ❌ PROBLEMA: No 404 route */}
                {/* ❌ PROBLEMA: No catch-all route */}
              </Routes>
            </Content>

            {/* ❌ PROBLEMA: Footer muy básico sin links útiles */}
            <Footer style={{ textAlign: "center", background: "#f0f2f5" }}>
              E-commerce Evolution ©2024 - Learning Project
              {/* ❌ PROBLEMA: No footer links (Privacy, Terms, etc.) */}
              {/* ❌ PROBLEMA: No social media links */}
              {/* ❌ PROBLEMA: No newsletter signup */}
            </Footer>
          </Layout>
        </CartProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
