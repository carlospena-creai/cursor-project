/**
 * LoadingFallback Component
 *
 * Componente de loading que se muestra mientras se cargan componentes lazy-loaded.
 * Usado con React Suspense.
 */

import React from "react";
import { Spin } from "antd";

const LoadingFallback: React.FC = () => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
      }}
    >
      <Spin size="large" tip="Cargando..." />
    </div>
  );
};

export default LoadingFallback;
