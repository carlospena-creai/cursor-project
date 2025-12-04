/**
 * ProductFormModal Component
 *
 * Modal para crear o editar un producto con validaciones.
 */
import React, { useEffect } from "react";
import { Modal, Form, Input, InputNumber, Switch, Select } from "antd";
import type { Product } from "../../Products/types/product.types";

const { TextArea } = Input;

interface ProductFormModalProps {
  open: boolean;
  product?: Product | null;
  loading?: boolean;
  onCancel: () => void;
  onFinish: (values: any) => Promise<void>;
}

export const ProductFormModal: React.FC<ProductFormModalProps> = ({
  open,
  product,
  loading = false,
  onCancel,
  onFinish,
}) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (open) {
      if (product) {
        form.setFieldsValue({
          name: product.name,
          description: product.description || "",
          price: product.price,
          stock: product.stock,
          category: product.category,
          is_active: product.is_active,
        });
      } else {
        form.resetFields();
      }
    }
  }, [open, product, form]);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await onFinish(values);
      form.resetFields();
    } catch (error) {
      console.error("Validation failed:", error);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onCancel();
  };

  return (
    <Modal
      title={product ? "Editar Producto" : "Crear Nuevo Producto"}
      open={open}
      onOk={handleSubmit}
      onCancel={handleCancel}
      confirmLoading={loading}
      okText={product ? "Actualizar" : "Crear"}
      cancelText="Cancelar"
      width={600}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          is_active: true,
          stock: 0,
        }}
      >
        <Form.Item
          name="name"
          label="Nombre del Producto"
          rules={[
            { required: true, message: "El nombre es requerido" },
            { min: 3, message: "El nombre debe tener al menos 3 caracteres" },
            { max: 200, message: "El nombre no puede exceder 200 caracteres" },
          ]}
        >
          <Input placeholder="Ingrese el nombre del producto" />
        </Form.Item>

        <Form.Item
          name="description"
          label="Descripción"
          rules={[
            {
              max: 1000,
              message: "La descripción no puede exceder 1000 caracteres",
            },
          ]}
        >
          <TextArea
            rows={4}
            placeholder="Ingrese la descripción del producto (opcional)"
          />
        </Form.Item>

        <Form.Item
          name="price"
          label="Precio"
          rules={[
            { required: true, message: "El precio es requerido" },
            {
              type: "number",
              message: "El precio debe ser un número",
            },
            {
              validator: (_, value) => {
                if (value === undefined || value === null) {
                  return Promise.resolve();
                }
                if (typeof value === "number" && value > 0) {
                  return Promise.resolve();
                }
                return Promise.reject(
                  new Error("El precio debe ser mayor que 0")
                );
              },
            },
          ]}
        >
          <InputNumber
            style={{ width: "100%" }}
            placeholder="0.00"
            prefix="$"
            min={0.01}
            step={0.01}
            precision={2}
          />
        </Form.Item>

        <Form.Item
          name="stock"
          label="Stock"
          rules={[
            { required: true, message: "El stock es requerido" },
            {
              type: "number",
              min: 0,
              message: "El stock debe ser mayor o igual a 0",
            },
            {
              validator: (_, value) => {
                if (value === undefined || value === null) {
                  return Promise.resolve();
                }
                if (Number.isInteger(value)) {
                  return Promise.resolve();
                }
                return Promise.reject(
                  new Error("El stock debe ser un número entero")
                );
              },
            },
          ]}
        >
          <InputNumber
            style={{ width: "100%" }}
            placeholder="0"
            min={0}
            step={1}
            parser={(value) => (value ? Math.floor(Number(value)) : "")}
          />
        </Form.Item>

        <Form.Item
          name="category"
          label="Categoría"
          rules={[
            { required: true, message: "La categoría es requerida" },
            {
              max: 100,
              message: "La categoría no puede exceder 100 caracteres",
            },
          ]}
        >
          <Select
            placeholder="Seleccione una categoría"
            showSearch
            filterOption={(input, option) =>
              (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
            }
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
        </Form.Item>

        <Form.Item name="is_active" label="Estado" valuePropName="checked">
          <Switch checkedChildren="Activo" unCheckedChildren="Inactivo" />
        </Form.Item>
      </Form>
    </Modal>
  );
};
