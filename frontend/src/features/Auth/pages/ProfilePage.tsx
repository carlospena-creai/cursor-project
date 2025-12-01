/**
 * ProfilePage
 *
 * Página de perfil del usuario con información y historial de órdenes.
 */
import React from "react";
import { Card, Typography, Space, Tag, Divider } from "antd";
import { UserOutlined, MailOutlined } from "@ant-design/icons";
import { useAuth } from "../context/AuthContext";
import { OrdersPage } from "../../Orders";

const { Title, Text } = Typography;

const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        My Profile
      </Title>

      <Card style={{ marginBottom: "24px" }}>
        <Space direction="vertical" size="large" style={{ width: "100%" }}>
          <div>
            <Title level={4}>
              <UserOutlined /> Account Information
            </Title>
            <Space direction="vertical" size="small">
              <div>
                <Text strong>Username: </Text>
                <Text>{user.username}</Text>
              </div>
              <div>
                <Text strong>
                  <MailOutlined /> Email:{" "}
                </Text>
                <Text>{user.email}</Text>
              </div>
              {user.full_name && (
                <div>
                  <Text strong>Full Name: </Text>
                  <Text>{user.full_name}</Text>
                </div>
              )}
              <div>
                <Text strong>Status: </Text>
                {user.is_active ? (
                  <Tag color="green">Active</Tag>
                ) : (
                  <Tag color="red">Inactive</Tag>
                )}
                {user.is_admin && <Tag color="blue">Administrator</Tag>}
              </div>
              <div>
                <Text strong>Member since: </Text>
                <Text>{formatDate(user.created_at)}</Text>
              </div>
            </Space>
          </div>
        </Space>
      </Card>

      <Divider />

      <Title level={3} style={{ marginBottom: "24px" }}>
        Order History
      </Title>
      <OrdersPage />
    </div>
  );
};

export default ProfilePage;
