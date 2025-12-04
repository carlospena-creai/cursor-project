/**
 * ProductsList Component
 *
 * Contenedor principal del feature de productos.
 * Utiliza Ant Design Row/Col para el grid layout.
 * Incluye paginación del servidor.
 */
import React, { useState, useMemo, useEffect } from "react";
import { Row, Col, Typography, Spin, Alert, Button, Pagination } from "antd";
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
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  // Memorizar los filtros con paginación
  const filters = useMemo(
    () => ({
      ...initialFilters,
      limit: pagination.pageSize,
      offset: (pagination.current - 1) * pagination.pageSize,
      only_active: true, // Solo mostrar productos activos en la tienda
    }),
    [initialFilters, pagination.pageSize, pagination.current]
  );

  const { products, total, loading, error, refetch } = useProducts(filters);

  // Actualizar el total de la paginación cuando cambian los productos
  useEffect(() => {
    setPagination((prev) => ({ ...prev, total: total }));
  }, [total]);

  // Resetear a la primera página cuando cambian los filtros iniciales (búsqueda, categoría, etc.)
  useEffect(() => {
    setPagination((prev) => ({ ...prev, current: 1 }));
  }, [initialFilters?.search, initialFilters?.category]);

  const handlePageChange = (page: number) => {
    setPagination({
      ...pagination,
      current: page,
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
        <>
          <Row gutter={[24, 24]}>
            {products.map((product) => (
              <Col key={product.id} xs={24} sm={12} md={8} lg={6}>
                <ProductCard product={product} />
              </Col>
            ))}
          </Row>
          {total > pagination.pageSize && (
            <div
              style={{
                marginTop: "32px",
                display: "flex",
                justifyContent: "center",
              }}
            >
              <Pagination
                current={pagination.current}
                pageSize={pagination.pageSize}
                total={total}
                showTotal={(total, range) =>
                  `Mostrando ${range[0]}-${range[1]} de ${total} productos`
                }
                onChange={handlePageChange}
              />
            </div>
          )}
        </>
      )}
    </div>
  );
};
