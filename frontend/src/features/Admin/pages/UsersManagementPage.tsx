/**
 * UsersManagementPage
 *
 * Página de gestión de usuarios para administradores.
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
  Input,
  Tooltip,
  Modal,
  Form,
  Switch,
} from "antd";
import {
  ReloadOutlined,
  EditOutlined,
  ClearOutlined,
  SearchOutlined,
} from "@ant-design/icons";
import type { ColumnsType, TableProps } from "antd/es/table";
import { useUsers } from "../hooks/useUsers";
import { useUsersManagement } from "../hooks/useUsersManagement";
import type { User, UsersFilters } from "../types/admin.types";

const { Title } = Typography;
const { Option } = Select;

const UsersManagementPage: React.FC = () => {
  const [isActiveFilter, setIsActiveFilter] = useState<boolean | null>(null);
  const [isAdminFilter, setIsAdminFilter] = useState<boolean | null>(null);
  const [searchText, setSearchText] = useState<string>("");
  const [sortField, setSortField] = useState<string | undefined>(undefined);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc" | undefined>(
    undefined
  );
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState<boolean>(false);
  const [form] = Form.useForm();

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  // Memorizar los filtros para evitar recrear el objeto en cada render
  const filters = useMemo<UsersFilters>(
    () => ({
      is_active: isActiveFilter,
      is_admin: isAdminFilter,
      search: searchText || undefined,
      limit: pagination.pageSize,
      offset: (pagination.current - 1) * pagination.pageSize,
      sort_by: sortField,
      sort_order: sortOrder,
    }),
    [
      isActiveFilter,
      isAdminFilter,
      searchText,
      pagination.pageSize,
      pagination.current,
      sortField,
      sortOrder,
    ]
  );

  const { users, total, loading, error, refetch } = useUsers(filters);
  const { updateUser, loading: actionLoading } = useUsersManagement();

  // Actualizar total en paginación cuando cambia
  useEffect(() => {
    setPagination((prev) => ({ ...prev, total }));
  }, [total]);

  // Actualizar paginación cuando cambian los filtros
  useEffect(() => {
    setPagination((prev) => ({ ...prev, current: 1 }));
  }, [isActiveFilter, isAdminFilter, searchText, sortField, sortOrder]);

  const handleEdit = (user: User) => {
    setSelectedUser(user);
    form.setFieldsValue({
      email: user.email,
      username: user.username,
      full_name: user.full_name || "",
      is_active: user.is_active,
      is_admin: user.is_admin,
    });
    setIsEditModalOpen(true);
  };

  const handleEditSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (!selectedUser) return;

      const updateData: Partial<User> = {};
      if (values.email !== selectedUser.email) updateData.email = values.email;
      if (values.username !== selectedUser.username)
        updateData.username = values.username;
      if (values.full_name !== selectedUser.full_name)
        updateData.full_name = values.full_name || null;
      if (values.is_active !== selectedUser.is_active)
        updateData.is_active = values.is_active;
      if (values.is_admin !== selectedUser.is_admin)
        updateData.is_admin = values.is_admin;

      await updateUser(selectedUser.id, updateData);
      setIsEditModalOpen(false);
      setSelectedUser(null);
      form.resetFields();
      refetch();
    } catch (error) {
      console.error("Error updating user:", error);
    }
  };

  const handleClearFilters = () => {
    setIsActiveFilter(null);
    setIsAdminFilter(null);
    setSearchText("");
    setSortField(undefined);
    setSortOrder(undefined);
  };

  const handleTableChange: TableProps<User>["onChange"] = (
    pag,
    tableFilters,
    sorter
  ) => {
    // Manejar paginación
    if (pag) {
      setPagination((prev) => ({
        ...prev,
        current: pag.current || 1,
        pageSize: pag.pageSize || 10,
      }));
    }

    // Manejar ordenamiento
    if (sorter && !Array.isArray(sorter)) {
      const { field, order } = sorter;
      if (field && order) {
        setSortField(field as string);
        setSortOrder(order === "ascend" ? "asc" : "desc");
      } else {
        setSortField(undefined);
        setSortOrder(undefined);
      }
    }
  };

  const columns: ColumnsType<User> = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      sorter: true,
      width: 80,
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
      sorter: true,
      ellipsis: true,
    },
    {
      title: "Username",
      dataIndex: "username",
      key: "username",
      sorter: true,
    },
    {
      title: "Nombre Completo",
      dataIndex: "full_name",
      key: "full_name",
      sorter: true,
      render: (text: string | null) => text || "-",
    },
    {
      title: "Estado",
      dataIndex: "is_active",
      key: "is_active",
      filters: [
        { text: "Activo", value: true },
        { text: "Inactivo", value: false },
      ],
      render: (isActive: boolean) => (
        <Tag color={isActive ? "green" : "red"}>
          {isActive ? "Activo" : "Inactivo"}
        </Tag>
      ),
    },
    {
      title: "Rol",
      dataIndex: "is_admin",
      key: "is_admin",
      filters: [
        { text: "Admin", value: true },
        { text: "Usuario", value: false },
      ],
      render: (isAdmin: boolean) => (
        <Tag color={isAdmin ? "purple" : "blue"}>
          {isAdmin ? "Admin" : "Usuario"}
        </Tag>
      ),
    },
    {
      title: "Fecha de Creación",
      dataIndex: "created_at",
      key: "created_at",
      sorter: true,
      render: (text: string | null) =>
        text ? new Date(text).toLocaleDateString() : "-",
    },
    {
      title: "Acciones",
      key: "actions",
      fixed: "right",
      width: 120,
      render: (_: any, record: User) => (
        <Space>
          <Tooltip title="Editar usuario">
            <Button
              type="primary"
              icon={<EditOutlined />}
              size="small"
              onClick={() => handleEdit(record)}
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
        <Button onClick={refetch} style={{ marginLeft: 8 }}>
          Reintentar
        </Button>
      </Card>
    );
  }

  return (
    <div>
      <Title level={2}>Gestión de Usuarios</Title>

      <Card>
        <Space direction="vertical" style={{ width: "100%" }} size="middle">
          {/* Filtros */}
          <Space wrap>
            <Input
              placeholder="Buscar por email, username o nombre..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: 300 }}
              allowClear
            />

            <Select
              placeholder="Estado"
              value={isActiveFilter}
              onChange={setIsActiveFilter}
              style={{ width: 150 }}
              allowClear
            >
              <Option value={true}>Activo</Option>
              <Option value={false}>Inactivo</Option>
            </Select>

            <Select
              placeholder="Rol"
              value={isAdminFilter}
              onChange={setIsAdminFilter}
              style={{ width: 150 }}
              allowClear
            >
              <Option value={true}>Admin</Option>
              <Option value={false}>Usuario</Option>
            </Select>

            <Button
              icon={<ClearOutlined />}
              onClick={handleClearFilters}
              disabled={!isActiveFilter && !isAdminFilter && !searchText}
            >
              Limpiar Filtros
            </Button>

            <Button
              icon={<ReloadOutlined />}
              onClick={refetch}
              loading={loading}
            >
              Actualizar
            </Button>
          </Space>

          {/* Tabla */}
          <Table
            columns={columns}
            dataSource={users}
            rowKey="id"
            loading={loading}
            pagination={{
              current: pagination.current,
              pageSize: pagination.pageSize,
              total: pagination.total,
              showTotal: (total, range) =>
                `${range[0]}-${range[1]} de ${total} usuarios`,
            }}
            onChange={handleTableChange}
            scroll={{ x: 1200 }}
          />
        </Space>
      </Card>

      {/* Modal de Edición */}
      <Modal
        title="Editar Usuario"
        open={isEditModalOpen}
        onOk={handleEditSubmit}
        onCancel={() => {
          setIsEditModalOpen(false);
          setSelectedUser(null);
          form.resetFields();
        }}
        confirmLoading={actionLoading}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: "El email es requerido" },
              { type: "email", message: "Email inválido" },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Username"
            name="username"
            rules={[
              { required: true, message: "El username es requerido" },
              {
                min: 3,
                message: "El username debe tener al menos 3 caracteres",
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item label="Nombre Completo" name="full_name">
            <Input />
          </Form.Item>

          <Form.Item label="Activo" name="is_active" valuePropName="checked">
            <Switch />
          </Form.Item>

          <Form.Item
            label="Administrador"
            name="is_admin"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UsersManagementPage;
