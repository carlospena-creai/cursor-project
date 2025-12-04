/**
 * AdminLayout Component
 *
 * Layout con navegación lateral para el panel administrativo.
 */
import React, { useState } from "react";
import { Layout, Menu, Typography, Button } from "antd";
import {
  DashboardOutlined,
  ShoppingOutlined,
  ContainerOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  ShopOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { useNavigate, useLocation } from "react-router-dom";

const { Sider, Content } = Layout;
const { Title } = Typography;

interface AdminLayoutProps {
  children: React.ReactNode;
}

const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: "/",
      icon: <ShopOutlined />,
      label: "Volver a la Tienda",
    },
    {
      type: "divider" as const,
    },
    {
      key: "/admin",
      icon: <DashboardOutlined />,
      label: "Dashboard",
    },
    {
      key: "/admin/products",
      icon: <ShoppingOutlined />,
      label: "Productos",
    },
    {
      key: "/admin/orders",
      icon: <ContainerOutlined />,
      label: "Órdenes",
    },
    {
      key: "/admin/users",
      icon: <UserOutlined />,
      label: "Usuarios",
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={250}
        style={{
          overflow: "auto",
          height: "100vh",
          position: "fixed",
          left: 0,
          top: 0,
          bottom: 0,
        }}
      >
        <div
          style={{
            height: 64,
            padding: "16px",
            display: "flex",
            alignItems: "center",
            justifyContent: collapsed ? "center" : "flex-start",
            borderBottom: "1px solid #f0f0f0",
          }}
        >
          {!collapsed && (
            <Title level={4} style={{ margin: 0, color: "#fff" }}>
              Admin Panel
            </Title>
          )}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout
        style={{ marginLeft: collapsed ? 80 : 250, transition: "all 0.2s" }}
      >
        <div
          style={{
            padding: "16px 24px",
            background: "#fff",
            borderBottom: "1px solid #f0f0f0",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: 16,
              width: 32,
              height: 32,
            }}
          />
        </div>
        <Content
          style={{
            margin: "24px",
            padding: 24,
            background: "#fff",
            minHeight: 280,
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default AdminLayout;
