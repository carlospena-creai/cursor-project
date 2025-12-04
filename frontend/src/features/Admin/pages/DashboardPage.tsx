/**
 * DashboardPage
 *
 * Página principal del panel administrativo con métricas y estadísticas.
 */
import React from "react";
import { Row, Col, Typography, Spin, Alert } from "antd";
import {
  ShoppingOutlined,
  ContainerOutlined,
  UserOutlined,
  DollarOutlined,
} from "@ant-design/icons";
import { useDashboardStats } from "../hooks/useDashboardStats";
import { StatsCard } from "../components/StatsCard";

const { Title } = Typography;

const DashboardPage: React.FC = () => {
  const { stats, loading, error, refetch } = useDashboardStats();

  if (error) {
    return (
      <Alert
        message="Error"
        description={error}
        type="error"
        showIcon
        action={
          <button onClick={refetch} style={{ marginLeft: 8 }}>
            Reintentar
          </button>
        }
      />
    );
  }

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        Dashboard Administrativo
      </Title>

      <Spin spinning={loading}>
        {stats && (
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Total Productos"
                value={stats.total_products}
                icon={<ShoppingOutlined />}
                color="#1890ff"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Productos Activos"
                value={stats.active_products}
                icon={<ShoppingOutlined />}
                color="#52c41a"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Total Órdenes"
                value={stats.total_orders}
                icon={<ContainerOutlined />}
                color="#722ed1"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Órdenes Pendientes"
                value={stats.pending_orders}
                icon={<ContainerOutlined />}
                color="#fa8c16"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Total Usuarios"
                value={stats.total_users}
                icon={<UserOutlined />}
                color="#13c2c2"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Usuarios Activos"
                value={stats.active_users}
                icon={<UserOutlined />}
                color="#52c41a"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Ingresos Totales"
                value={stats.total_revenue}
                suffix="$"
                icon={<DollarOutlined />}
                color="#52c41a"
                loading={loading}
              />
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <StatsCard
                title="Órdenes Recientes"
                value={stats.recent_orders_count}
                icon={<ContainerOutlined />}
                color="#1890ff"
                loading={loading}
              />
            </Col>
          </Row>
        )}
      </Spin>
    </div>
  );
};

export default DashboardPage;
