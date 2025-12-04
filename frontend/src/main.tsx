import React from "react";
import ReactDOM from "react-dom/client";
import { ConfigProvider } from "antd";
import App from "./App.tsx";
import "./index.css";

// ✅ Ant Design theme mejorado con customización empresarial
// ❌ PROBLEMA: No configuración de locale/internacionalización
// ✅ Error boundaries globales implementados en App.tsx
const theme = {
  token: {
    colorPrimary: "#1890ff",
    borderRadius: 6,
    fontFamily:
      "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
    fontSize: 14,
    lineHeight: 1.6,
  },
  components: {
    Button: {
      borderRadius: 6,
      fontWeight: 500,
      controlHeight: 40,
    },
    Card: {
      borderRadius: 12,
      paddingLG: 24,
    },
    Input: {
      borderRadius: 6,
      controlHeight: 40,
    },
    Table: {
      borderRadius: 8,
    },
    Modal: {
      borderRadius: 12,
    },
    Message: {
      contentPadding: "12px 16px",
    },
    Notification: {
      borderRadius: 8,
    },
  },
  // ❌ PROBLEMA: No dark mode support
  // ❌ PROBLEMA: No responsive breakpoints customizados
};

// ❌ PROBLEMA: No configuración de performance monitoring
// ❌ PROBLEMA: No configuración de error reporting (Sentry, etc.)
// ❌ PROBLEMA: No configuración de analytics
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConfigProvider theme={theme}>
      {/* ✅ Error boundary wrapper implementado en App.tsx */}
      {/* ✅ Loading provider global con Suspense en App.tsx */}
      {/* ❌ PROBLEMA: No notification provider global */}
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
