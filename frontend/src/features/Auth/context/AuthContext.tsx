/**
 * Auth Context
 *
 * Context API para manejar el estado global de autenticación.
 * Proporciona funciones para login, register, logout y acceso al usuario actual.
 */
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import { authApi } from "../utils/authApi";
import apiClient from "@shared/services/apiClient";
import type {
  AuthContextType,
  LoginRequest,
  RegisterRequest,
  User,
} from "../types/auth.types";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_STORAGE_KEY = "auth_token";
const USER_STORAGE_KEY = "auth_user";

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(() => {
    // Cargar usuario desde localStorage al inicializar
    try {
      const savedUser = localStorage.getItem(USER_STORAGE_KEY);
      return savedUser ? JSON.parse(savedUser) : null;
    } catch (error) {
      console.error("Error loading user from localStorage:", error);
      return null;
    }
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  });

  const [loading, setLoading] = useState(true);

  // Verificar token y cargar perfil al montar
  useEffect(() => {
    const initializeAuth = async () => {
      const savedToken = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (savedToken) {
        try {
          // Verificar que el token sigue siendo válido obteniendo el perfil
          const userProfile = await authApi.getProfile();
          setUser(userProfile);
          setToken(savedToken);
          // Actualizar token en apiClient
          apiClient.setAuthToken(savedToken);
        } catch (error) {
          // Token inválido o expirado
          console.error("Token validation failed:", error);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  // Guardar token y usuario en localStorage cuando cambien
  useEffect(() => {
    if (token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
      apiClient.setAuthToken(token);
    } else {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      apiClient.removeAuthToken();
    }
  }, [token]);

  useEffect(() => {
    if (user) {
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(USER_STORAGE_KEY);
    }
  }, [user]);

  const login = useCallback(async (credentials: LoginRequest) => {
    try {
      setLoading(true);
      const response = await authApi.login(credentials);

      setToken(response.access_token);
      setUser(response.user);
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(
    async (data: RegisterRequest) => {
      try {
        setLoading(true);
        const newUser = await authApi.register(data);

        // Después de registrar, hacer login automático
        await login({
          email_or_username: data.email,
          password: data.password,
        });
      } catch (error) {
        console.error("Register error:", error);
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [login]
  );

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
    apiClient.removeAuthToken();
  }, []);

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isAdmin: user?.is_admin || false,
    login,
    register,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
