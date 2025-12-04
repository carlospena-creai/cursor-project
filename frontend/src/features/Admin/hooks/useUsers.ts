/**
 * useUsers Hook
 *
 * Hook personalizado para obtener y gestionar usuarios con filtros, paginación y ordenamiento.
 */
import { useState, useEffect, useCallback } from "react";
import { usersAdminApi } from "../utils/usersApi";
import type { User, UsersFilters } from "../types/admin.types";

interface UseUsersReturn {
  users: User[];
  total: number;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useUsers = (filters?: UsersFilters): UseUsersReturn => {
  const [users, setUsers] = useState<User[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await usersAdminApi.getUsers(filters);
      setUsers(response.users);
      setTotal(response.total);
    } catch (err: any) {
      const errorMessage =
        err?.response?.data?.detail ||
        err?.message ||
        "Error al obtener usuarios";
      setError(errorMessage);
      setUsers([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [
    filters?.is_active,
    filters?.is_admin,
    filters?.search,
    filters?.limit,
    filters?.offset,
    filters?.sort_by,
    filters?.sort_order,
  ]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return {
    users,
    total,
    loading,
    error,
    refetch: fetchUsers,
  };
};
