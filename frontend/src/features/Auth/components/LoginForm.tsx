/**
 * LoginForm Component
 *
 * Formulario de login con validación.
 */
import React, { useState } from "react";
import { Form, Input, Button, Card, Typography, Alert, Space } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

const { Title, Text } = Typography;

export const LoginForm: React.FC = () => {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [form] = Form.useForm();

  const handleSubmit = async (values: {
    email_or_username: string;
    password: string;
  }) => {
    try {
      setError(null);
      await login(values);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <Card style={{ maxWidth: 400, margin: "0 auto", marginTop: "50px" }}>
      <Space direction="vertical" size="large" style={{ width: "100%" }}>
        <div style={{ textAlign: "center" }}>
          <Title level={2}>Login</Title>
          <Text type="secondary">Sign in to your account</Text>
        </div>

        {error && <Alert message={error} type="error" showIcon />}

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          size="large"
        >
          <Form.Item
            name="email_or_username"
            label="Email or Username"
            rules={[
              {
                required: true,
                message: "Please enter your email or username",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Email or username"
              autoComplete="username"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[{ required: true, message: "Please enter your password" }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Password"
              autoComplete="current-password"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              Sign In
            </Button>
          </Form.Item>
        </Form>

        <div style={{ textAlign: "center" }}>
          <Text type="secondary">
            Don't have an account? <Link to="/register">Register here</Link>
          </Text>
        </div>
      </Space>
    </Card>
  );
};
