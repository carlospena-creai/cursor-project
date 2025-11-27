/**
 * ProductsList Component
 *
 * Contenedor principal del feature de productos.
 * Utiliza Ant Design Row/Col para el grid layout.
 */
import React, { useState } from "react";
import {
  Row,
  Col,
  Typography,
  Spin,
  Alert,
  Input,
  Select,
  Button,
  Space,
} from "antd";
import { useProducts } from "../hooks/useProducts";
import { ProductCard } from "./ProductCard";
import type { ProductsFilters } from "../types/product.types";

const { Title } = Typography;
const { Search } = Input;

interface ProductsListProps {
  initialFilters?: ProductsFilters;
  title?: string;
}

export const ProductsList: React.FC<ProductsListProps> = ({
  initialFilters,
  title = "Featured Products",
}) => {
  const { products, loading, error, refetch, setFilters } =
    useProducts(initialFilters);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  const handleSearch = (value: string) => {
    setSearch(value);
    setFilters({
      ...initialFilters,
      search: value || undefined,
      category: category || undefined,
    });
  };

  const handleCategoryChange = (value: string) => {
    setCategory(value);
    setFilters({
      ...initialFilters,
      search: search || undefined,
      category: value || undefined,
    });
  };

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
      <div
        style={{
          marginBottom: "24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "16px",
        }}
      >
        <Title level={2} style={{ margin: 0 }}>
          {title}
        </Title>

        <Space wrap>
          <Search
            placeholder="Search products..."
            allowClear
            onSearch={handleSearch}
            style={{ width: 200 }}
          />

          <Select
            placeholder="Category"
            allowClear
            value={category || undefined}
            onChange={handleCategoryChange}
            style={{ width: 150 }}
          >
            <Select.Option value="">All Categories</Select.Option>
            <Select.Option value="Electronics">Electronics</Select.Option>
            <Select.Option value="Home">Home</Select.Option>
            <Select.Option value="Sports">Sports</Select.Option>
            <Select.Option value="Clothing">Clothing</Select.Option>
          </Select>
        </Space>
      </div>

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
