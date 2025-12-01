/**
 * OrderList Component
 *
 * Componente para mostrar una lista de órdenes.
 */
import React from "react";
import { Spin, Empty, Alert } from "antd";
import { OrderCard } from "./OrderCard";
import type { Order } from "../types/order.types";

interface OrderListProps {
  orders: Order[];
  loading?: boolean;
  error?: string | null;
}

export const OrderList: React.FC<OrderListProps> = ({
  orders,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "50px" }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  if (orders.length === 0) {
    return <Empty description="No orders found" />;
  }

  return (
    <div>
      {orders.map((order) => (
        <OrderCard key={order.id} order={order} />
      ))}
    </div>
  );
};
