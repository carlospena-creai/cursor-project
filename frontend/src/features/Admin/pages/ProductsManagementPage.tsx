/**
 * ProductsManagementPage
 *
 * Página de gestión de productos para administradores.
 * Incluye Data Table con CRUD completo, filtros, búsqueda y bulk operations.
 */
import React, { useState, useMemo, useEffect } from "react";
import {
  Table,
  Button,
  Space,
  Input,
  Select,
  Tag,
  Popconfirm,
  Typography,
  Card,
  Row,
  Col,
  Tooltip,
  message,
} from "antd";
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  SearchOutlined,
  ClearOutlined,
} from "@ant-design/icons";
import type { ColumnsType, TableProps } from "antd/es/table";
import { useProducts } from "../../Products/hooks/useProducts";
import { useProductsManagement } from "../hooks/useProductsManagement";
import { ProductFormModal } from "../components/ProductFormModal";
import type { Product } from "../../Products/types/product.types";

const { Title } = Typography;
const { Search } = Input;

const ProductsManagementPage: React.FC = () => {
  const [searchText, setSearchText] = useState<string>("");
  const [categoryFilter, setCategoryFilter] = useState<string | undefined>(
    undefined
  );
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [showOnlyActive, setShowOnlyActive] = useState<boolean>(true);

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  });

  // Memorizar los filtros para evitar recrear el objeto en cada render
  const filters = useMemo(
    () => ({
      search: searchText || undefined,
      category: categoryFilter,
      limit: pagination.pageSize,
      offset: (pagination.current - 1) * pagination.pageSize,
      only_active: showOnlyActive,
    }),
    [
      searchText,
      categoryFilter,
      pagination.pageSize,
      pagination.current,
      showOnlyActive,
    ]
  );

  const { products, total, loading, error, refetch } = useProducts(filters);

  const {
    loading: actionLoading,
    createProduct,
    updateProduct,
    deleteProduct,
    bulkDelete,
  } = useProductsManagement();

  // Los productos ya vienen filtrados del servidor según showOnlyActive
  // No necesitamos filtrar localmente
  const filteredProducts = products;

  // Actualizar paginación cuando cambian los filtros
  useEffect(() => {
    setPagination((prev) => ({ ...prev, current: 1 }));
  }, [searchText, categoryFilter, showOnlyActive]);

  const handleCreate = async (values: any) => {
    const result = await createProduct(values);
    if (result) {
      setIsModalOpen(false);
      setEditingProduct(null);
      refetch();
    }
  };

  const handleUpdate = async (values: any) => {
    if (!editingProduct) return;
    const result = await updateProduct(editingProduct.id, values);
    if (result) {
      setIsModalOpen(false);
      setEditingProduct(null);
      refetch();
    }
  };

  const handleDelete = async (id: number) => {
    const result = await deleteProduct(id);
    if (result) {
      refetch();
    }
  };

  const handleBulkDelete = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning("Por favor seleccione al menos un producto");
      return;
    }

    const result = await bulkDelete({
      product_ids: selectedRowKeys.map((key) => Number(key)),
    });
    if (result) {
      setSelectedRowKeys([]);
      refetch();
    }
  };

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setIsModalOpen(true);
  };

  const handleNew = () => {
    setEditingProduct(null);
    setIsModalOpen(true);
  };

  const handleClearFilters = () => {
    setSearchText("");
    setCategoryFilter(undefined);
    setShowOnlyActive(true);
  };

  const rowSelection: TableProps<Product>["rowSelection"] = {
    selectedRowKeys,
    onChange: (keys) => setSelectedRowKeys(keys),
    getCheckboxProps: (record) => ({
      disabled: !record.is_active,
    }),
  };

  const columns: ColumnsType<Product> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
      sorter: (a, b) => a.id - b.id,
    },
    {
      title: "Nombre",
      dataIndex: "name",
      key: "name",
      sorter: (a, b) => a.name.localeCompare(b.name),
      render: (text, record) => (
        <div>
          <div style={{ fontWeight: 500 }}>{text}</div>
          {record.description && (
            <div style={{ fontSize: "12px", color: "#8c8c8c", marginTop: 4 }}>
              {record.description.length > 50
                ? `${record.description.substring(0, 50)}...`
                : record.description}
            </div>
          )}
        </div>
      ),
    },
    {
      title: "Categoría",
      dataIndex: "category",
      key: "category",
      width: 120,
      filters: [
        { text: "Electronics", value: "Electronics" },
        { text: "Clothing", value: "Clothing" },
        { text: "Home", value: "Home" },
        { text: "Sports", value: "Sports" },
        { text: "Books", value: "Books" },
        { text: "Toys", value: "Toys" },
        { text: "Food", value: "Food" },
        { text: "Other", value: "Other" },
      ],
      onFilter: (value, record) => record.category === value,
      render: (category) => <Tag color="blue">{category}</Tag>,
    },
    {
      title: "Precio",
      dataIndex: "price",
      key: "price",
      width: 120,
      sorter: (a, b) => a.price - b.price,
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: "Stock",
      dataIndex: "stock",
      key: "stock",
      width: 100,
      sorter: (a, b) => a.stock - b.stock,
      render: (stock) => (
        <Tag color={stock > 10 ? "green" : stock > 0 ? "orange" : "red"}>
          {stock}
        </Tag>
      ),
    },
    {
      title: "Estado",
      dataIndex: "is_active",
      key: "is_active",
      width: 100,
      filters: [
        { text: "Activo", value: true },
        { text: "Inactivo", value: false },
      ],
      onFilter: (value, record) => record.is_active === value,
      render: (isActive) => (
        <Tag color={isActive ? "green" : "red"}>
          {isActive ? "Activo" : "Inactivo"}
        </Tag>
      ),
    },
    {
      title: "Acciones",
      key: "actions",
      width: 150,
      fixed: "right",
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="Editar">
            <Button
              type="link"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
              size="small"
            />
          </Tooltip>
          <Popconfirm
            title="¿Eliminar este producto?"
            description="Esta acción no se puede deshacer."
            onConfirm={() => handleDelete(record.id)}
            okText="Sí, eliminar"
            cancelText="Cancelar"
            okType="danger"
          >
            <Tooltip title="Eliminar">
              <Button
                type="link"
                danger
                icon={<DeleteOutlined />}
                size="small"
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  if (error) {
    return (
      <Card>
        <Typography.Text type="danger">{error}</Typography.Text>
        <Button onClick={refetch} style={{ marginLeft: 16 }}>
          Reintentar
        </Button>
      </Card>
    );
  }

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2} style={{ margin: 0 }}>
            Gestión de Productos
          </Title>
        </Col>
        <Col>
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={refetch}
              loading={loading}
            >
              Actualizar
            </Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleNew}>
              Nuevo Producto
            </Button>
          </Space>
        </Col>
      </Row>

      <Card>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col xs={24} sm={12} md={8}>
            <Search
              placeholder="Buscar productos..."
              allowClear
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onSearch={() => refetch()}
              prefix={<SearchOutlined />}
              style={{ width: "100%" }}
            />
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Filtrar por categoría"
              allowClear
              value={categoryFilter}
              onChange={setCategoryFilter}
              style={{ width: "100%" }}
              options={[
                { value: "Electronics", label: "Electronics" },
                { value: "Clothing", label: "Clothing" },
                { value: "Home", label: "Home" },
                { value: "Sports", label: "Sports" },
                { value: "Books", label: "Books" },
                { value: "Toys", label: "Toys" },
                { value: "Food", label: "Food" },
                { value: "Other", label: "Other" },
              ]}
            />
          </Col>
          <Col xs={24} sm={12} md={4}>
            <Select
              value={showOnlyActive ? "active" : "all"}
              onChange={(value) => setShowOnlyActive(value === "active")}
              style={{ width: "100%" }}
              options={[
                { value: "active", label: "Solo Activos" },
                { value: "all", label: "Todos" },
              ]}
            />
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Space>
              {(searchText || categoryFilter) && (
                <Button icon={<ClearOutlined />} onClick={handleClearFilters}>
                  Limpiar Filtros
                </Button>
              )}
              {selectedRowKeys.length > 0 && (
                <Popconfirm
                  title={`¿Eliminar ${selectedRowKeys.length} producto(s) seleccionado(s)?`}
                  description="Esta acción no se puede deshacer."
                  onConfirm={handleBulkDelete}
                  okText="Sí, eliminar"
                  cancelText="Cancelar"
                  okType="danger"
                >
                  <Button
                    danger
                    icon={<DeleteOutlined />}
                    loading={actionLoading}
                  >
                    Eliminar Seleccionados ({selectedRowKeys.length})
                  </Button>
                </Popconfirm>
              )}
            </Space>
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={filteredProducts}
          rowKey="id"
          loading={loading || actionLoading}
          rowSelection={rowSelection}
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: total,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} de ${total} productos`,
            onChange: (page) => {
              setPagination({
                ...pagination,
                current: page,
              });
            },
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <ProductFormModal
        open={isModalOpen}
        product={editingProduct}
        loading={actionLoading}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingProduct(null);
        }}
        onFinish={editingProduct ? handleUpdate : handleCreate}
      />
    </div>
  );
};

export default ProductsManagementPage;
