/**
 * RegisterForm Component
 *
 * Formulario de registro con validación.
 */
import React, { useState } from "react";
import { Form, Input, Button, Card, Typography, Alert, Space } from "antd";
import { UserOutlined, LockOutlined, MailOutlined } from "@ant-design/icons";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

const { Title, Text } = Typography;

export const RegisterForm: React.FC = () => {
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [form] = Form.useForm();

  const handleSubmit = async (values: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
  }) => {
    try {
      setError(null);
      await register(values);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    }
  };

  return (
    <Card style={{ maxWidth: 400, margin: "0 auto", marginTop: "50px" }}>
      <Space direction="vertical" size="large" style={{ width: "100%" }}>
        <div style={{ textAlign: "center" }}>
          <Title level={2}>Register</Title>
          <Text type="secondary">Create a new account</Text>
        </div>

        {error && <Alert message={error} type="error" showIcon />}

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          size="large"
        >
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: "Please enter your email" },
              { type: "email", message: "Please enter a valid email" },
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="Email"
              autoComplete="email"
            />
          </Form.Item>

          <Form.Item
            name="username"
            label="Username"
            rules={[
              { required: true, message: "Please enter a username" },
              { min: 3, message: "Username must be at least 3 characters" },
              {
                pattern: /^[a-zA-Z0-9_-]+$/,
                message:
                  "Username can only contain letters, numbers, hyphens and underscores",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Username"
              autoComplete="username"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[
              { required: true, message: "Please enter a password" },
              { min: 8, message: "Password must be at least 8 characters" },
              {
                pattern: /^(?=.*[A-Za-z])(?=.*\d)/,
                message:
                  "Password must contain at least one letter and one number",
              },
            ]}
            hasFeedback
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Password"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item
            name="confirm"
            label="Confirm Password"
            dependencies={["password"]}
            hasFeedback
            rules={[
              { required: true, message: "Please confirm your password" },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue("password") === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error("Passwords do not match"));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Confirm password"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item
            name="full_name"
            label="Full Name (Optional)"
            rules={[
              { min: 2, message: "Full name must be at least 2 characters" },
            ]}
          >
            <Input placeholder="Full name" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              Create Account
            </Button>
          </Form.Item>
        </Form>

        <div style={{ textAlign: "center" }}>
          <Text type="secondary">
            Already have an account? <Link to="/login">Login here</Link>
          </Text>
        </div>
      </Space>
    </Card>
  );
};
