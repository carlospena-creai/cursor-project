/**
 * CheckoutPage
 *
 * Página para completar el checkout y crear una orden.
 */
import React from "react";
import {
  Row,
  Col,
  Typography,
  Form,
  Input,
  Button,
  Card,
  Alert,
  message,
} from "antd";
import { useCart } from "../context/CartContext";
import { useCreateOrder } from "../hooks/useCreateOrder";
import { CartSummary } from "../components/CartSummary";
import { CartItem } from "../components/CartItem";
import { useNavigate } from "react-router-dom";

const { Title } = Typography;
const { TextArea } = Input;

const CheckoutPage: React.FC = () => {
  const { items, clearCart } = useCart();
  const { createOrder, loading, error } = useCreateOrder();
  const navigate = useNavigate();
  const [form] = Form.useForm();

  // TODO: Obtener user_id del contexto de autenticación cuando esté disponible
  // Por ahora usamos un valor por defecto
  const userId = 1;

  const handleSubmit = async (values: {
    shipping_address?: string;
    notes?: string;
  }) => {
    if (items.length === 0) {
      message.error("Your cart is empty");
      return;
    }

    const orderData = {
      user_id: userId,
      items: items.map((item) => ({
        product_id: item.productId,
        quantity: item.quantity,
      })),
      shipping_address: values.shipping_address,
      notes: values.notes,
    };

    const order = await createOrder(orderData);

    if (order) {
      message.success("Order created successfully!");
      clearCart();
      navigate("/orders");
    }
  };

  if (items.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "50px" }}>
        <Title level={3}>Your cart is empty</Title>
        <Button type="primary" onClick={() => navigate("/")}>
          Continue Shopping
        </Button>
      </div>
    );
  }

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        Checkout
      </Title>

      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: "24px" }}
        />
      )}

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <Card title="Order Details" style={{ marginBottom: "24px" }}>
            {items.map((item) => (
              <CartItem key={item.productId} item={item} />
            ))}
          </Card>

          <Card title="Shipping Information">
            <Form form={form} layout="vertical" onFinish={handleSubmit}>
              <Form.Item
                name="shipping_address"
                label="Shipping Address"
                rules={[
                  {
                    required: true,
                    message: "Please enter your shipping address",
                  },
                  {
                    max: 500,
                    message: "Address must be less than 500 characters",
                  },
                ]}
              >
                <TextArea
                  rows={4}
                  placeholder="Enter your complete shipping address"
                />
              </Form.Item>

              <Form.Item
                name="notes"
                label="Order Notes (Optional)"
                rules={[
                  {
                    max: 1000,
                    message: "Notes must be less than 1000 characters",
                  },
                ]}
              >
                <TextArea
                  rows={3}
                  placeholder="Any special instructions or notes for your order"
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  size="large"
                  block
                  loading={loading}
                >
                  Place Order
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <CartSummary onCheckout={() => form.submit()} />
        </Col>
      </Row>
    </div>
  );
};

export default CheckoutPage;
