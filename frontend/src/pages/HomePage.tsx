import React from "react";
import { Typography } from "antd";
import { ProductsList } from "../features/Products";

const { Title, Paragraph, Text } = Typography;

const HomePage: React.FC = () => {
  return (
    <div>
      {/* Hero Section */}
      <div
        style={{
          background: "linear-gradient(135deg, #1890ff 0%, #096dd9 100%)",
          padding: "60px 0",
          borderRadius: "8px",
          marginBottom: "40px",
          color: "white",
          textAlign: "center",
        }}
      >
        <Title level={1} style={{ color: "white", margin: 0 }}>
          Welcome to E-commerce Evolution
        </Title>
        <Paragraph
          style={{ fontSize: "18px", color: "white", margin: "16px 0" }}
        >
          This is the base project that will evolve into a full-featured
          e-commerce platform
        </Paragraph>
        <Text style={{ color: "white", opacity: 0.9 }}>
          🚀 Day 2: Products connected with the real API
        </Text>
      </div>

      {/* Products Section - Using Products Feature */}
      <ProductsList title="Featured Products" />

      {/* Info Section */}
      <div
        style={{
          marginTop: "60px",
          padding: "40px",
          background: "white",
          borderRadius: "8px",
          textAlign: "center",
        }}
      >
        <Title level={3}>Project Evolution Timeline</Title>
        {/* Timeline will be implemented in future days */}
      </div>
    </div>
  );
};

export default HomePage;
