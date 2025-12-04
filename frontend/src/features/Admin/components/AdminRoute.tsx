/**
 * AdminRoute Component
 *
 * Componente para proteger rutas de administración.
 * Solo permite acceso a usuarios con rol de administrador.
 */
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../Auth/context/AuthContext";

interface AdminRouteProps {
  children: React.ReactNode;
}

export const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!user?.is_admin) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};
