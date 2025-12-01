/**
 * ProtectedRoute Component
 *
 * Componente para proteger rutas que requieren autenticación.
 * Redirige al login si el usuario no está autenticado.
 */
import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { Spin } from "antd";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requireAdmin = false,
}) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "50px" }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirigir al login guardando la ubicación actual
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requireAdmin && !isAdmin) {
    // Redirigir si se requiere admin pero el usuario no es admin
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};
