/**
 * CartItem Component
 *
 * Componente para mostrar un item del carrito con opciones para actualizar cantidad o eliminar.
 */
import React from "react";
import { Card, InputNumber, Button, Space, Typography } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import { useCart } from "../context/CartContext";
import type { CartItem as CartItemType } from "../types/order.types";

const { Text } = Typography;

interface CartItemProps {
  item: CartItemType;
}

export const CartItem: React.FC<CartItemProps> = ({ item }) => {
  const { updateQuantity, removeItem } = useCart();

  const handleQuantityChange = (value: number | null) => {
    if (value !== null && value > 0) {
      updateQuantity(item.productId, value);
    }
  };

  const handleRemove = () => {
    removeItem(item.productId);
  };

  return (
    <Card
      style={{ marginBottom: "16px" }}
      actions={[
        <Button
          key="remove"
          danger
          icon={<DeleteOutlined />}
          onClick={handleRemove}
        >
          Remove
        </Button>,
      ]}
    >
      <Space direction="vertical" style={{ width: "100%" }} size="small">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Text strong>{item.productName}</Text>
          <Text strong style={{ fontSize: "16px" }}>
            ${item.subtotal.toFixed(2)}
          </Text>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Space>
            <Text>Quantity:</Text>
            <InputNumber
              min={1}
              max={999}
              value={item.quantity}
              onChange={handleQuantityChange}
              style={{ width: "80px" }}
            />
          </Space>
          <Text type="secondary">${item.unitPrice.toFixed(2)} each</Text>
        </div>
      </Space>
    </Card>
  );
};
