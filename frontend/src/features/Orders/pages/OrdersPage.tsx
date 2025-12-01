/**
 * OrdersPage
 *
 * Página para mostrar todas las órdenes del usuario.
 */
import React from "react";
import { Typography } from "antd";
import { useOrders } from "../hooks/useOrders";
import { OrderList } from "../components/OrderList";

const { Title } = Typography;

const OrdersPage: React.FC = () => {
  // TODO: Obtener user_id del contexto de autenticación cuando esté disponible
  // Por ahora usamos un valor por defecto
  const userId = 1;

  const { orders, loading, error } = useOrders({ user_id: userId });

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
