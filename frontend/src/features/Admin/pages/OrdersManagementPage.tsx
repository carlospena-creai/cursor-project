/**
 * OrdersManagementPage
 *
 * Página de gestión de órdenes para administradores.
 * Incluye Data Table con filtros, ordenamiento y acciones.
 */
import React, { useState, useMemo, useEffect } from "react";
import {
  Table,
  Button,
  Space,
  Select,
  Tag,
  Typography,
  Card,
  Row,
  Col,
  Tooltip,
  Modal,
  Descriptions,
} from "antd";
import {
  ReloadOutlined,
  EyeOutlined,
  EditOutlined,
  ClearOutlined,
} from "@ant-design/icons";
import type { ColumnsType } from "antd/es/table";
import { useOrders } from "../../Orders/hooks/useOrders";
import { useOrdersManagement } from "../hooks/useOrdersManagement";
import type { Order, OrderStatus } from "../../Orders/types/order.types";

const { Title } = Typography;

const ORDER_STATUS_OPTIONS: { value: OrderStatus; label: string; color: string }[] =
  [
    { value: "pending", label: "Pendiente", color: "orange" },
    { value: "confirmed", label: "Confirmada", color: "blue" },
    { value: "processing", label: "En Proceso", color: "cyan" },
    { value: "shipped", label: "Enviada", color: "purple" },
    { value: "delivered", label: "Entregada", color: "green" },
    { value: "cancelled", label: "Cancelada", color: "red" },
  ];

const OrdersManagementPage: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState<OrderStatus | undefined>(
    undefined
  );
  const [sortField, setSortField] = useState<string | undefined>(undefined);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc" | undefined>(
    undefined
  );
  const [tableFilters, setTableFilters] = useState<{
    status?: OrderStatus[];
  }>({});
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState<boolean>(false);
  const [isStatusModalOpen, setIsStatusModalOpen] = useState<boolean>(false);

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  });

  // Memorizar los filtros para evitar recrear el objeto en cada render
  const filters = useMemo(
    () => ({
      status: statusFilter,
      limit: pagination.pageSize,
      offset: (pagination.current - 1) * pagination.pageSize,
      sort_by: sortField,
      sort_order: sortOrder,
    }),
    [
      statusFilter,
      pagination.pageSize,
      pagination.current,
      sortField,
      sortOrder,
    ]
  );

  const { orders, total, loading, error, refetch } = useOrders(filters);

  const {
    loading: actionLoading,
    updateOrderStatus,
  } = useOrdersManagement();

  // Actualizar paginación cuando cambian los filtros
  useEffect(() => {
    setPagination((prev) => ({ ...prev, current: 1 }));
  }, [statusFilter, sortField, sortOrder]);

  const handleViewDetails = (order: Order) => {
    setSelectedOrder(order);
    setIsDetailModalOpen(true);
  };

  const handleUpdateStatus = (order: Order) => {
    setSelectedOrder(order);
    setIsStatusModalOpen(true);
  };

  const handleStatusChange = async (newStatus: OrderStatus) => {
    if (!selectedOrder) return;

    const result = await updateOrderStatus(selectedOrder.id!, newStatus);
    if (result) {
      setIsStatusModalOpen(false);
      setSelectedOrder(null);
      refetch();
    }
  };

  const handleClearFilters = () => {
    setStatusFilter(undefined);
    setTableFilters({});
    setSortField(undefined);
    setSortOrder(undefined);
  };

  const handleTableChange = (
    pag: any,
    filters: Record<string, any>,
    sorter: any
  ) => {
    // Manejar paginación
    setPagination({
      current: pag.current,
      pageSize: pag.pageSize,
    });

    // Manejar filtros de la tabla
    const newFilters: { status?: OrderStatus[] } = {};
    if (filters.status) {
      newFilters.status = filters.status as OrderStatus[];
      setStatusFilter(
        filters.status.length > 0 ? (filters.status[0] as OrderStatus) : undefined
      );
    } else {
      setStatusFilter(undefined);
    }

    setTableFilters(newFilters);

    // Manejar ordenamiento
    if (sorter && sorter.field) {
      setSortField(sorter.field);
      setSortOrder(sorter.order === "ascend" ? "asc" : "desc");
    } else {
      setSortField(undefined);
      setSortOrder(undefined);
    }
  };

  const getStatusColor = (status: OrderStatus): string => {
    const option = ORDER_STATUS_OPTIONS.find((opt) => opt.value === status);
    return option?.color || "default";
  };

  const getStatusLabel = (status: OrderStatus): string => {
    const option = ORDER_STATUS_OPTIONS.find((opt) => opt.value === status);
    return option?.label || status;
  };

  const getAvailableStatuses = (currentStatus: OrderStatus): OrderStatus[] => {
    // Transiciones válidas según el modelo de dominio
    const validTransitions: Record<OrderStatus, OrderStatus[]> = {
      pending: ["confirmed", "cancelled"],
      confirmed: ["processing", "cancelled"],
      processing: ["shipped", "cancelled"],
      shipped: ["delivered"],
      delivered: [],
      cancelled: [],
    };

    return validTransitions[currentStatus] || [];
  };

  const columns: ColumnsType<Order> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
      sorter: true,
    },
    {
      title: "Usuario ID",
      dataIndex: "user_id",
      key: "user_id",
      width: 100,
      sorter: true,
    },
    {
      title: "Items",
      key: "items",
      width: 150,
      render: (_, record) => (
        <Tooltip
          title={record.items.map((item) => `${item.product_name} x${item.quantity}`).join(", ")}
        >
          <span>{record.items.length} producto(s)</span>
        </Tooltip>
      ),
    },
    {
      title: "Estado",
      dataIndex: "status",
      key: "status",
      width: 120,
      filters: ORDER_STATUS_OPTIONS.map((opt) => ({
        text: opt.label,
        value: opt.value,
      })),
      filteredValue: tableFilters.status,
      render: (status: OrderStatus) => (
        <Tag color={getStatusColor(status)}>{getStatusLabel(status)}</Tag>
      ),
    },
    {
      title: "Total",
      dataIndex: "total",
      key: "total",
      width: 120,
      sorter: true,
      render: (total: number) => `$${total.toFixed(2)}`,
    },
    {
      title: "Fecha",
      dataIndex: "created_at",
      key: "created_at",
      width: 180,
      sorter: true,
      render: (date: string | null) =>
        date ? new Date(date).toLocaleString("es-ES") : "-",
    },
    {
      title: "Acciones",
      key: "actions",
      width: 150,
      fixed: "right",
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="Ver Detalles">
            <Button
              type="link"
              icon={<EyeOutlined />}
              onClick={() => handleViewDetails(record)}
              size="small"
            />
          </Tooltip>
          <Tooltip title="Actualizar Estado">
            <Button
              type="link"
              icon={<EditOutlined />}
              onClick={() => handleUpdateStatus(record)}
              size="small"
              disabled={getAvailableStatuses(record.status).length === 0}
            />
          </Tooltip>
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
            Gestión de Órdenes
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
          </Space>
        </Col>
      </Row>

      <Card>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col xs={24} sm={12} md={8}>
            <Select
              placeholder="Filtrar por estado"
              allowClear
              style={{ width: "100%" }}
              onChange={(value) => setStatusFilter(value || undefined)}
              value={statusFilter}
              options={ORDER_STATUS_OPTIONS.map((opt) => ({
                value: opt.value,
                label: opt.label,
              }))}
            />
          </Col>
          <Col xs={24} sm={12} md={8}>
            {statusFilter && (
              <Button icon={<ClearOutlined />} onClick={handleClearFilters}>
                Limpiar Filtros
              </Button>
            )}
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={orders}
          rowKey="id"
          loading={loading || actionLoading}
          onChange={handleTableChange}
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: total,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} de ${total} órdenes`,
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* Modal de Detalles */}
      <Modal
        title="Detalles de la Orden"
        open={isDetailModalOpen}
        onCancel={() => {
          setIsDetailModalOpen(false);
          setSelectedOrder(null);
        }}
        footer={[
          <Button
            key="close"
            onClick={() => {
              setIsDetailModalOpen(false);
              setSelectedOrder(null);
            }}
          >
            Cerrar
          </Button>,
          <Button
            key="update"
            type="primary"
            onClick={() => {
              setIsDetailModalOpen(false);
              if (selectedOrder) {
                handleUpdateStatus(selectedOrder);
              }
            }}
            disabled={
              selectedOrder
                ? getAvailableStatuses(selectedOrder.status).length === 0
                : true
            }
          >
            Actualizar Estado
          </Button>,
        ]}
        width={800}
      >
        {selectedOrder && (
          <Descriptions bordered column={1}>
            <Descriptions.Item label="ID">{selectedOrder.id}</Descriptions.Item>
            <Descriptions.Item label="Usuario ID">
              {selectedOrder.user_id}
            </Descriptions.Item>
            <Descriptions.Item label="Estado">
              <Tag color={getStatusColor(selectedOrder.status)}>
                {getStatusLabel(selectedOrder.status)}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="Total">
              ${selectedOrder.total.toFixed(2)}
            </Descriptions.Item>
            <Descriptions.Item label="Dirección de Envío">
              {selectedOrder.shipping_address || "No especificada"}
            </Descriptions.Item>
            <Descriptions.Item label="Notas">
              {selectedOrder.notes || "Sin notas"}
            </Descriptions.Item>
            <Descriptions.Item label="Fecha de Creación">
              {selectedOrder.created_at
                ? new Date(selectedOrder.created_at).toLocaleString("es-ES")
                : "-"}
            </Descriptions.Item>
            <Descriptions.Item label="Última Actualización">
              {selectedOrder.updated_at
                ? new Date(selectedOrder.updated_at).toLocaleString("es-ES")
                : "-"}
            </Descriptions.Item>
            <Descriptions.Item label="Items">
              <Table
                dataSource={selectedOrder.items}
                rowKey="id"
                pagination={false}
                size="small"
                columns={[
                  {
                    title: "Producto",
                    dataIndex: "product_name",
                    key: "product_name",
                  },
                  {
                    title: "Cantidad",
                    dataIndex: "quantity",
                    key: "quantity",
                    width: 100,
                  },
                  {
                    title: "Precio Unitario",
                    dataIndex: "unit_price",
                    key: "unit_price",
                    width: 120,
                    render: (price: number) => `$${price.toFixed(2)}`,
                  },
                  {
                    title: "Subtotal",
                    dataIndex: "subtotal",
                    key: "subtotal",
                    width: 120,
                    render: (subtotal: number) => `$${subtotal.toFixed(2)}`,
                  },
                ]}
              />
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      {/* Modal de Actualizar Estado */}
      <Modal
        title="Actualizar Estado de la Orden"
        open={isStatusModalOpen}
        onCancel={() => {
          setIsStatusModalOpen(false);
          setSelectedOrder(null);
        }}
        footer={null}
      >
        {selectedOrder && (
          <div>
            <p>
              Estado actual:{" "}
              <Tag color={getStatusColor(selectedOrder.status)}>
                {getStatusLabel(selectedOrder.status)}
              </Tag>
            </p>
            <p style={{ marginBottom: 16 }}>
              Seleccione el nuevo estado:
            </p>
            <Space direction="vertical" style={{ width: "100%" }}>
              {getAvailableStatuses(selectedOrder.status).map((status) => {
                const option = ORDER_STATUS_OPTIONS.find(
                  (opt) => opt.value === status
                );
                return (
                  <Button
                    key={status}
                    type="default"
                    block
                    onClick={() => handleStatusChange(status)}
                    loading={actionLoading}
                  >
                    {option?.label || status}
                  </Button>
                );
              })}
              {getAvailableStatuses(selectedOrder.status).length === 0 && (
                <Typography.Text type="secondary">
                  No hay transiciones de estado disponibles para esta orden.
                </Typography.Text>
              )}
            </Space>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default OrdersManagementPage;

