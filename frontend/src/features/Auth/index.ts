/**
 * Auth Feature - Public Exports
 *
 * Exporta todos los componentes, hooks y utilidades del feature de autenticación.
 */

// Pages
export { default as LoginPage } from "./pages/LoginPage";
export { default as RegisterPage } from "./pages/RegisterPage";
export { default as ProfilePage } from "./pages/ProfilePage";

// Components
export { LoginForm } from "./components/LoginForm";
export { RegisterForm } from "./components/RegisterForm";
export { ProtectedRoute } from "./components/ProtectedRoute";

// Context
export { AuthProvider, useAuth } from "./context/AuthContext";

// Types
export type {
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  AuthContextType,
} from "./types/auth.types";

// Utils
export { authApi } from "./utils/authApi";
