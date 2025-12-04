/**
 * MainLayout Component
 *
 * Layout principal para las rutas normales de la aplicación.
 * Incluye header y footer.
 */
import React from "react";
import {
  Layout,
  Input,
  Button,
  Row,
  Col,
  Typography,
  Space,
  message,
} from "antd";
import {
  FacebookOutlined,
  TwitterOutlined,
  InstagramOutlined,
  LinkedinOutlined,
} from "@ant-design/icons";
import AppHeader from "./Header";

const { Content, Footer } = Layout;
const { Text } = Typography;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <AppHeader />
      {/* ✅ Content padding responsive */}
      <Content
        style={{
          padding: "24px",
          minHeight: "calc(100vh - 64px - 70px)",
        }}
        className="fade-in"
      >
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            width: "100%",
          }}
        >
          {/* ✅ Error boundary wrapper implementado en App.tsx */}
          {/* ✅ Loading fallback para suspense implementado en App.tsx */}
          {children}
        </div>
      </Content>
      <Footer
        style={{
          background: "#f0f2f5",
          padding: "40px 50px 24px",
          borderTop: "1px solid #e8e8e8",
        }}
      >
        <Row gutter={[32, 32]}>
          {/* Links útiles */}
          <Col xs={24} sm={12} md={6}>
            <Text strong style={{ display: "block", marginBottom: 12 }}>
              Enlaces
            </Text>
            <Space direction="vertical" size="small" style={{ width: "100%" }}>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Página de Privacidad - Próximamente");
                }}
                style={{ color: "#666", textDecoration: "none" }}
              >
                Privacidad
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Términos y Condiciones - Próximamente");
                }}
                style={{ color: "#666", textDecoration: "none" }}
              >
                Términos y Condiciones
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Sobre Nosotros - Próximamente");
                }}
                style={{ color: "#666", textDecoration: "none" }}
              >
                Sobre Nosotros
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Contacto - Próximamente");
                }}
                style={{ color: "#666", textDecoration: "none" }}
              >
                Contacto
              </a>
            </Space>
          </Col>

          {/* Newsletter */}
          <Col xs={24} sm={12} md={10}>
            <Text strong style={{ display: "block", marginBottom: 12 }}>
              Newsletter
            </Text>
            <Text
              type="secondary"
              style={{ display: "block", marginBottom: 12, fontSize: 12 }}
            >
              Suscríbete para recibir ofertas exclusivas y novedades
            </Text>
            <Space.Compact style={{ width: "100%" }}>
              <Input
                placeholder="Tu email"
                type="email"
                style={{ maxWidth: 250 }}
              />
              <Button
                type="primary"
                onClick={() => {
                  message.success(
                    "¡Gracias por suscribirte! (Solo UI - Backend no implementado)"
                  );
                }}
              >
                Suscribirse
              </Button>
            </Space.Compact>
          </Col>

          {/* Redes Sociales */}
          <Col xs={24} sm={12} md={8}>
            <Text strong style={{ display: "block", marginBottom: 12 }}>
              Síguenos
            </Text>
            <Space size="large">
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Facebook - Próximamente");
                }}
                style={{ color: "#666", fontSize: 24 }}
              >
                <FacebookOutlined />
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Twitter - Próximamente");
                }}
                style={{ color: "#666", fontSize: 24 }}
              >
                <TwitterOutlined />
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("Instagram - Próximamente");
                }}
                style={{ color: "#666", fontSize: 24 }}
              >
                <InstagramOutlined />
              </a>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  message.info("LinkedIn - Próximamente");
                }}
                style={{ color: "#666", fontSize: 24 }}
              >
                <LinkedinOutlined />
              </a>
            </Space>
          </Col>
        </Row>

        <div
          style={{
            textAlign: "center",
            marginTop: 32,
            paddingTop: 24,
            borderTop: "1px solid #e8e8e8",
            color: "#666",
            fontSize: 14,
          }}
        >
          E-commerce Evolution ©2024 - Learning Project
        </div>
      </Footer>
    </Layout>
  );
};

export default MainLayout;
