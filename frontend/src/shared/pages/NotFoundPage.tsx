/**
 * NotFoundPage Component
 *
 * Página 404 personalizada que se muestra cuando el usuario intenta acceder
 * a una ruta que no existe en la aplicación.
 */

import React from "react";
import { Result, Button } from "antd";
import { useNavigate } from "react-router-dom";
import { HomeOutlined, ArrowLeftOutlined } from "@ant-design/icons";

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate("/");
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <Result
      status="404"
      title="404"
      subTitle="Lo sentimos, la página que buscas no existe."
      extra={[
        <Button
          type="primary"
          key="home"
          icon={<HomeOutlined />}
          onClick={handleGoHome}
          size="large"
        >
          Ir al Inicio
        </Button>,
        <Button
          key="back"
          icon={<ArrowLeftOutlined />}
          onClick={handleGoBack}
          size="large"
        >
          Volver Atrás
        </Button>,
      ]}
    />
  );
};

export default NotFoundPage;
