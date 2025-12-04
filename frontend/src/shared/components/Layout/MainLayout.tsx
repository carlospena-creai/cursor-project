/**
 * MainLayout Component
 *
 * Layout principal para las rutas normales de la aplicación.
 * Incluye header y footer.
 */
import React from "react";
import { Layout } from "antd";
import AppHeader from "./Header";

const { Content, Footer } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <AppHeader />
      {/* ❌ PROBLEMA: Content padding hardcodeado sin responsiveness */}
      <Content style={{ padding: "24px 50px" }}>
        {/* ❌ PROBLEMA: No error boundary wrapper para rutas */}
        {/* ❌ PROBLEMA: No loading fallback para suspense */}
        {children}
      </Content>
      <Footer style={{ textAlign: "center", background: "#f0f2f5" }}>
        E-commerce Evolution ©2024 - Learning Project
        {/* ❌ PROBLEMA: No footer links (Privacy, Terms, etc.) */}
        {/* ❌ PROBLEMA: No social media links */}
        {/* ❌ PROBLEMA: No newsletter signup */}
      </Footer>
    </Layout>
  );
};

export default MainLayout;
