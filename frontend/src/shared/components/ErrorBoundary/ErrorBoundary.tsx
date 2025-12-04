/**
 * ErrorBoundary Component
 *
 * Componente para capturar errores de JavaScript en cualquier parte del árbol de componentes.
 * Muestra un fallback UI en lugar de que la aplicación se rompa completamente.
 *
 * ✅ Implementa componentDidCatch y getDerivedStateFromError
 * ✅ Proporciona información útil para debugging
 * ✅ Permite resetear el error y reintentar
 */

import React, { Component, ErrorInfo, ReactNode } from "react";
import { Result, Button, Card, Typography, Space, Collapse } from "antd";
import { ReloadOutlined, BugOutlined, HomeOutlined } from "@ant-design/icons";

const { Paragraph, Text } = Typography;
const { Panel } = Collapse;

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  resetKeys?: Array<string | number>;
  resetOnPropsChange?: boolean;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * ErrorBoundary Component
 *
 * Captura errores en el árbol de componentes hijo y muestra un fallback UI.
 */
class ErrorBoundaryClass extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Actualiza el estado para que el siguiente render muestre el fallback UI
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Registra el error para debugging
    console.error("ErrorBoundary caught an error:", error, errorInfo);

    this.setState({
      error,
      errorInfo,
    });

    // Llama al callback si está definido (útil para logging externo como Sentry)
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  componentDidUpdate(prevProps: Props) {
    // Resetear el error si las props de reset cambian
    if (this.props.resetOnPropsChange && this.props.resetKeys) {
      const hasResetKeyChanged = this.props.resetKeys.some(
        (key, index) => key !== prevProps.resetKeys?.[index]
      );

      if (hasResetKeyChanged && this.state.hasError) {
        this.resetErrorBoundary();
      }
    }
  }

  resetErrorBoundary = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      // Si hay un fallback personalizado, usarlo
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Fallback UI por defecto
      return (
        <ErrorFallbackContent
          error={this.state.error}
          errorInfo={this.state.errorInfo}
          onReset={this.resetErrorBoundary}
        />
      );
    }

    return this.props.children;
  }
}

/**
 * ErrorFallback Component
 *
 * UI que se muestra cuando ocurre un error.
 */
interface ErrorFallbackProps {
  error: Error | null;
  errorInfo: ErrorInfo | null;
  onReset: () => void;
}

const ErrorFallbackContent: React.FC<ErrorFallbackProps> = ({
  error,
  errorInfo,
  onReset,
}) => {
  const handleGoHome = () => {
    window.location.href = "/";
  };

  const handleReload = () => {
    window.location.reload();
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "24px",
        background: "#f0f2f5",
      }}
    >
      <Card
        style={{
          maxWidth: 800,
          width: "100%",
        }}
      >
        <Result
          status="error"
          icon={<BugOutlined style={{ color: "#ff4d4f" }} />}
          title="¡Oops! Algo salió mal"
          subTitle="Ha ocurrido un error inesperado. Por favor, intenta nuevamente o contacta al soporte si el problema persiste."
          extra={
            <Space>
              <Button
                type="primary"
                icon={<ReloadOutlined />}
                onClick={onReset}
                size="large"
              >
                Reintentar
              </Button>
              <Button
                icon={<HomeOutlined />}
                onClick={handleGoHome}
                size="large"
              >
                Ir al Inicio
              </Button>
              <Button onClick={handleReload} size="large">
                Recargar Página
              </Button>
            </Space>
          }
        >
          {error && (
            <div style={{ marginTop: 24 }}>
              <Collapse>
                <Panel header="Detalles del Error (para debugging)" key="1">
                  <Space direction="vertical" style={{ width: "100%" }}>
                    <div>
                      <Text strong>Mensaje de Error:</Text>
                      <Paragraph
                        code
                        style={{
                          marginTop: 8,
                          background: "#f5f5f5",
                          padding: "8px 12px",
                          borderRadius: 4,
                          display: "block",
                        }}
                      >
                        {error.message}
                      </Paragraph>
                    </div>

                    {error.stack && (
                      <div>
                        <Text strong>Stack Trace:</Text>
                        <pre
                          style={{
                            marginTop: 8,
                            background: "#f5f5f5",
                            padding: "12px",
                            borderRadius: 4,
                            overflow: "auto",
                            maxHeight: 200,
                            fontSize: 12,
                          }}
                        >
                          {error.stack}
                        </pre>
                      </div>
                    )}

                    {errorInfo && errorInfo.componentStack && (
                      <div>
                        <Text strong>Component Stack:</Text>
                        <pre
                          style={{
                            marginTop: 8,
                            background: "#f5f5f5",
                            padding: "12px",
                            borderRadius: 4,
                            overflow: "auto",
                            maxHeight: 200,
                            fontSize: 12,
                          }}
                        >
                          {errorInfo.componentStack}
                        </pre>
                      </div>
                    )}
                  </Space>
                </Panel>
              </Collapse>
            </div>
          )}
        </Result>
      </Card>
    </div>
  );
};

/**
 * ErrorBoundary Hook Wrapper
 *
 * Wrapper funcional para usar ErrorBoundary con hooks de React Router
 */
export const ErrorBoundary: React.FC<Props> = (props) => {
  return <ErrorBoundaryClass {...props} />;
};

export default ErrorBoundary;
