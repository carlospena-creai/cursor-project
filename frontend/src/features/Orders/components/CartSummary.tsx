/**
 * CartSummary Component
 *
 * Componente para mostrar el resumen del carrito con total y acciones.
 */
import React from "react";
import { Card, Button, Space, Typography, Divider } from "antd";
import { ShoppingCartOutlined } from "@ant-design/icons";
import { useCart } from "../context/CartContext";
import { useNavigate } from "react-router-dom";

const { Title, Text } = Typography;

interface CartSummaryProps {
  onCheckout?: () => void;
}

export const CartSummary: React.FC<CartSummaryProps> = ({ onCheckout }) => {
  const { items, getTotal, getItemCount, clearCart } = useCart();
  const navigate = useNavigate();

  const total = getTotal();
  const itemCount = getItemCount();

  const handleCheckout = () => {
    if (onCheckout) {
      onCheckout();
    } else {
      navigate("/checkout");
    }
  };

  if (items.length === 0) {
    return (
      <Card>
        <Space
          direction="vertical"
          align="center"
          style={{ width: "100%", padding: "20px" }}
        >
          <ShoppingCartOutlined
            style={{ fontSize: "48px", color: "#d9d9d9" }}
          />
          <Text type="secondary">Your cart is empty</Text>
        </Space>
      </Card>
    );
  }

  return (
    <Card>
      <Space direction="vertical" style={{ width: "100%" }} size="large">
        <Title level={4}>Cart Summary</Title>

        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <Text>Items ({itemCount}):</Text>
          <Text strong>${total.toFixed(2)}</Text>
        </div>

        <Divider />

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Title level={4} style={{ margin: 0 }}>
            Total:
          </Title>
          <Title level={4} style={{ margin: 0, color: "#1890ff" }}>
            ${total.toFixed(2)}
          </Title>
        </div>

        <Space direction="vertical" style={{ width: "100%" }} size="small">
          <Button type="primary" block size="large" onClick={handleCheckout}>
            Proceed to Checkout
          </Button>
          <Button block onClick={clearCart}>
            Clear Cart
          </Button>
        </Space>
      </Space>
    </Card>
  );
};
