/**
 * OrdersPage
 *
 * Página para mostrar todas las órdenes del usuario.
 */
import React from "react";
import { Typography } from "antd";
import { useOrders } from "../hooks/useOrders";
import { OrderList } from "../components/OrderList";
import { useAuth } from "../../Auth/context/AuthContext";

const { Title } = Typography;

const OrdersPage: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  const { orders, loading, error } = useOrders();

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        My Orders
      </Title>

      <OrderList orders={orders} loading={loading} error={error} />
    </div>
  );
};

export default OrdersPage;
