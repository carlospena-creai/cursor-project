/**
 * useUsersManagement Hook
 *
 * Hook personalizado para gestionar usuarios en el panel de administración.
 * Proporciona funciones para actualizar usuarios.
 */
import { useState } from "react";
import { message } from "antd";
import { usersAdminApi } from "../utils/usersApi";
import type { User, UserUpdate } from "../types/admin.types";

export const useUsersManagement = () => {
  const [loading, setLoading] = useState(false);

  /**
   * Actualiza un usuario existente
   */
  const updateUser = async (
    userId: number,
    data: UserUpdate
  ): Promise<User | null> => {
    setLoading(true);
    try {
      const updatedUser = await usersAdminApi.updateUser(userId, data);
      message.success("Usuario actualizado correctamente");
      return updatedUser;
    } catch (error: any) {
      const errorMessage =
        error?.response?.data?.detail ||
        error?.message ||
        "Error al actualizar usuario";
      message.error(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    updateUser,
    loading,
  };
};
