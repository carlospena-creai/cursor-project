/**
 * OrderCard Component
 *
 * Componente para mostrar una orden individual con sus detalles.
 */
import React from "react";
import { Card, Tag, Typography, Space, Divider, List } from "antd";
import type { Order } from "../types/order.types";

const { Text } = Typography;

interface OrderCardProps {
  order: Order;
}

const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    pending: "orange",
    confirmed: "blue",
    processing: "cyan",
    shipped: "purple",
    delivered: "green",
    cancelled: "red",
  };
  return colors[status] || "default";
};

export const OrderCard: React.FC<OrderCardProps> = ({ order }) => {
  const formatDate = (dateString: string | null | undefined): string => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <Card
      style={{ marginBottom: "16px" }}
      title={
        <Space>
          <Text strong>Order #{order.id}</Text>
          <Tag color={getStatusColor(order.status)}>
            {order.status.toUpperCase()}
          </Tag>
        </Space>
      }
      extra={<Text strong>${order.total.toFixed(2)}</Text>}
    >
      <Space direction="vertical" style={{ width: "100%" }} size="middle">
        <div>
          <Text type="secondary">Items:</Text>
          <List
            size="small"
            dataSource={order.items}
            renderItem={(item) => (
              <List.Item>
                <Space
                  style={{ width: "100%", justifyContent: "space-between" }}
                >
                  <Text>
                    {item.product_name} x {item.quantity}
                  </Text>
                  <Text strong>${item.subtotal.toFixed(2)}</Text>
                </Space>
              </List.Item>
            )}
          />
        </div>

        {order.shipping_address && (
          <div>
            <Text type="secondary">Shipping Address:</Text>
            <br />
            <Text>{order.shipping_address}</Text>
          </div>
        )}

        {order.notes && (
          <div>
            <Text type="secondary">Notes:</Text>
            <br />
            <Text>{order.notes}</Text>
          </div>
        )}

        <Divider style={{ margin: "8px 0" }} />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "12px",
          }}
        >
          <Text type="secondary">Created: {formatDate(order.created_at)}</Text>
          {order.updated_at && order.updated_at !== order.created_at && (
            <Text type="secondary">
              Updated: {formatDate(order.updated_at)}
            </Text>
          )}
        </div>
      </Space>
    </Card>
  );
};
