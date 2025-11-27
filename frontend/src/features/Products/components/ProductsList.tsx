/**
 * ProductsList Component
 *
 * Contenedor principal del feature de productos.
 * Utiliza Ant Design Row/Col para el grid layout.
 */
import React from "react";
import { Row, Col, Typography, Spin, Alert, Button } from "antd";
import { useProducts } from "../hooks/useProducts";
import { ProductCard } from "./ProductCard";
import type { ProductsFilters } from "../types/product.types";

const { Title } = Typography;

interface ProductsListProps {
  initialFilters?: ProductsFilters;
  title?: string;
}

export const ProductsList: React.FC<ProductsListProps> = ({
  initialFilters,
  title = "Featured Products",
}) => {
  const { products, loading, error, refetch } = useProducts(initialFilters);

  if (error) {
    return (
      <Alert
        message="Error loading products"
        description={error}
        type="error"
        action={
          <Button size="small" onClick={() => refetch()}>
            Retry
          </Button>
        }
        style={{ marginBottom: "24px" }}
      />
    );
  }

  return (
    <div>
      {title && (
        <Title level={2} style={{ margin: 0, marginBottom: "24px" }}>
          {title}
        </Title>
      )}

      {loading ? (
        <div style={{ textAlign: "center", padding: "40px" }}>
          <Spin size="large" />
          <p style={{ marginTop: "16px" }}>Loading products...</p>
        </div>
      ) : products.length === 0 ? (
        <Alert
          message="No products found"
          description="Try adjusting your filters or check back later."
          type="info"
        />
      ) : (
        <Row gutter={[24, 24]}>
          {products.map((product) => (
            <Col key={product.id} xs={24} sm={12} md={8} lg={6}>
              <ProductCard product={product} />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};
