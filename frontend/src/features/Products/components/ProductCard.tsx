/**
 * ProductCard Component
 *
 * Componente presentacional basado en Ant Design Card.
 * Muestra la información de un producto en formato de tarjeta.
 */
import React from "react";
import { Card, Typography, Tag } from "antd";
import type { Product } from "../types";

const { Title, Paragraph } = Typography;
const { Meta } = Card;

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  // Generar imagen placeholder basada en categoría
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      Electronics: "1890ff",
      Home: "52c41a",
      Sports: "722ed1",
      Clothing: "fa8c16",
    };
    return colors[category] || "13c2c2";
  };

  const imageUrl = `https://via.placeholder.com/300x200/${getCategoryColor(
    product.category
  )}/white?text=${encodeURIComponent(product.name)}`;

  return (
    <Card
      hoverable
      style={{ height: "100%" }}
      cover={
        <div style={{ height: "200px", overflow: "hidden" }}>
          <img
            alt={product.name}
            src={imageUrl}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </div>
      }
    >
      <Meta
        title={
          <div>
            <div style={{ marginBottom: "8px" }}>{product.name}</div>
            <Tag color="blue">{product.category}</Tag>
            {product.stock === 0 && (
              <Tag color="red" style={{ marginLeft: "8px" }}>
                Out of Stock
              </Tag>
            )}
          </div>
        }
        description={
          <div>
            <Paragraph
              ellipsis={{ rows: 2 }}
              style={{ margin: "8px 0", color: "#666" }}
            >
              {product.description || "No description available"}
            </Paragraph>
            <Title level={4} style={{ margin: 0, color: "#1890ff" }}>
              ${product.price.toFixed(2)}
            </Title>
            {product.stock > 0 && (
              <Paragraph
                style={{ margin: "8px 0 0 0", fontSize: "12px", color: "#999" }}
              >
                Stock: {product.stock}
              </Paragraph>
            )}
          </div>
        }
      />
    </Card>
  );
};
