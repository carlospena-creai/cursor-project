/**
 * CartPage
 *
 * Página para mostrar y gestionar el carrito de compras.
 */
import React from "react";
import { Row, Col, Typography } from "antd";
import { ShoppingCartOutlined } from "@ant-design/icons";
import { useCart } from "../context/CartContext";
import { CartItem } from "../components/CartItem";
import { CartSummary } from "../components/CartSummary";

const { Title } = Typography;

const CartPage: React.FC = () => {
  const { items } = useCart();

  if (items.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "50px" }}>
        <ShoppingCartOutlined
          style={{ fontSize: "64px", color: "#d9d9d9", marginBottom: "16px" }}
        />
        <Title level={3}>Your cart is empty</Title>
        <p style={{ color: "#999" }}>Add some products to get started!</p>
      </div>
    );
  }

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        Shopping Cart
      </Title>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <div>
            {items.map((item) => (
              <CartItem key={item.productId} item={item} />
            ))}
          </div>
        </Col>

        <Col xs={24} lg={8}>
          <CartSummary />
        </Col>
      </Row>
    </div>
  );
};

export default CartPage;
