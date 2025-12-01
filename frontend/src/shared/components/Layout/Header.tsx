import React, { useState, useEffect } from "react";
import {
  Layout,
  Menu,
  Badge,
  Button,
  Space,
  Typography,
  Input,
  Select,
  Flex,
} from "antd";
import {
  ShoppingCartOutlined,
  UserOutlined,
  ShopOutlined,
  HeartOutlined,
  SearchOutlined,
} from "@ant-design/icons";
import { useNavigate, useLocation } from "react-router-dom";
import { useCart } from "../../../features/Orders/context/CartContext";

const { Header } = Layout;
const { Title } = Typography;
const { Search } = Input;

// ❌ PROBLEMA: Componente muy grande - should be split into smaller components
// ❌ PROBLEMA: No memoization con React.memo para performance
// ❌ PROBLEMA: No configuración responsive apropiada para mobile
const AppHeader: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { getItemCount } = useCart();
  const [searchValue, setSearchValue] = useState("");
  const [categoryValue, setCategoryValue] = useState<string | undefined>(
    undefined
  );

  // ✅ ACTUALIZADO: Usa Cart Context para obtener el contador real
  const cartItemsCount = getItemCount();
  const isAuthenticated = false; // Will come from auth context in Day 4
  const wishlistCount = 0; // Will be implemented later

  // ❌ PROBLEMA: Menu items hardcodeados - should be configurable
  // ❌ PROBLEMA: No role-based menu filtering
  // ❌ PROBLEMA: No menu items activos/inactivos por permisos
  const menuItems = [
    {
      key: "/",
      icon: <ShopOutlined />,
      label: "Products",
      onClick: () => navigate("/"),
    },
    {
      key: "/orders",
      icon: <ShopOutlined />,
      label: "Orders",
      onClick: () => navigate("/orders"),
    },
    // TODO Day 4: Profile, Login
    // TODO Day 5: Admin (if admin user)
  ];

  // ✅ ACTUALIZADO: Navega al carrito
  const handleCartClick = () => {
    navigate("/cart");
  };

  const handleWishlistClick = () => {
    console.log("Wishlist clicked - will be implemented later");
    // ❌ PROBLEMA: No implementación de wishlist
    // ❌ PROBLEMA: No persistencia local de wishlist
    // navigate('/wishlist')
  };

  const handleLoginClick = () => {
    console.log("Login clicked - will navigate to login in Day 4");
    // ❌ PROBLEMA: No redirect apropiado después del login
    // navigate('/login') // Will be implemented in Day 4
  };

  const handleProfileClick = () => {
    console.log("Profile clicked - will navigate to profile in Day 4");
    // ❌ PROBLEMA: No dropdown con opciones de perfil
    // navigate('/profile') // Will be implemented in Day 4
  };

  const handleSearch = (value: string) => {
    const params = new URLSearchParams();
    if (value) params.append("q", value);
    if (categoryValue) params.append("category", categoryValue);
    navigate(`/search?${params.toString()}`);
  };

  const handleCategoryChange = (value: string) => {
    setCategoryValue(value || undefined);
    const params = new URLSearchParams();
    if (searchValue) params.append("q", searchValue);
    if (value) params.append("category", value);
    navigate(`/search?${params.toString()}`);
  };

  // Sync search and category values with URL parameters when on search page
  useEffect(() => {
    if (location.pathname === "/search") {
      const params = new URLSearchParams(location.search);
      const q = params.get("q") || "";
      const category = params.get("category") || undefined;
      setSearchValue(q);
      setCategoryValue(category);
    } else {
      // Clear search values when not on search page
      setSearchValue("");
      setCategoryValue(undefined);
    }
  }, [location.pathname, location.search]);

  // ❌ PROBLEMA: Return muy grande - should be split into render functions
  // ❌ PROBLEMA: Estilos inline - should use CSS-in-JS or styled components
  return (
    <Header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 24px",
        background: "#fff",
        borderBottom: "1px solid #f0f0f0",
        // ❌ PROBLEMA: No box-shadow para depth
        // ❌ PROBLEMA: No sticky behavior
      }}
    >
      {/* ❌ PROBLEMA: Logo and Navigation section muy grande */}
      <div style={{ display: "flex", alignItems: "center", flex: 1 }}>
        {/* ❌ PROBLEMA: Logo hardcodeado - should be configurable */}
        {/* ❌ PROBLEMA: No logo image - just emoji */}
        {/* ❌ PROBLEMA: No hover effects en logo */}
        <Title
          level={3}
          style={{
            margin: 0,
            marginRight: "32px",
            color: "#1890ff",
            cursor: "pointer",
            // ❌ PROBLEMA: No transition effects
          }}
          onClick={() => navigate("/")}
        >
          🛒 E-commerce
        </Title>

        {/* ❌ PROBLEMA: Menu sin configuración avanzada */}
        {/* ❌ PROBLEMA: No mobile hamburger menu */}
        {/* ❌ PROBLEMA: No keyboard navigation support */}
        <Menu
          theme="light"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          style={{
            border: "none",
            background: "transparent",
            flex: 1,
            // ❌ PROBLEMA: No custom styling para active items
          }}
        />
      </div>

      {/* ❌ PROBLEMA: Right Side Actions sin responsive behavior */}
      {/* ❌ PROBLEMA: No collapse en mobile */}
      <Flex gap={"middle"}>
        {/* Search Bar and Category Filter */}
        <Search
          placeholder="Search products..."
          allowClear
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onSearch={handleSearch}
          style={{ width: 200 }}
          enterButton={<SearchOutlined />}
        />
        <Select
          placeholder="Category"
          allowClear
          value={categoryValue}
          onChange={handleCategoryChange}
          style={{ width: 150 }}
        >
          <Select.Option value="">All Categories</Select.Option>
          <Select.Option value="Electronics">Electronics</Select.Option>
          <Select.Option value="Home">Home</Select.Option>
          <Select.Option value="Sports">Sports</Select.Option>
          <Select.Option value="Clothing">Clothing</Select.Option>
        </Select>

        {/* ❌ PROBLEMA: Wishlist sin implementación */}
        {/* ❌ PROBLEMA: Badge sin animación cuando cambia el count */}
        <Badge count={wishlistCount} size="small">
          <Button
            type="text"
            icon={<HeartOutlined />}
            onClick={handleWishlistClick}
            // ❌ PROBLEMA: No tooltip describiendo la funcionalidad
          />
        </Badge>

        {/* ❌ PROBLEMA: Shopping Cart sin preview del contenido */}
        {/* ❌ PROBLEMA: No dropdown preview del carrito */}
        <Badge count={cartItemsCount} size="small">
          <Button
            type="text"
            icon={<ShoppingCartOutlined />}
            onClick={handleCartClick}
            // ❌ PROBLEMA: No loading state cuando se actualiza el carrito
          />
        </Badge>

        {/* ❌ PROBLEMA: User Authentication muy básico */}
        {/* ❌ PROBLEMA: No dropdown con opciones cuando está autenticado */}
        {/* ❌ PROBLEMA: No avatar del usuario */}
        {isAuthenticated ? (
          <Button
            type="text"
            icon={<UserOutlined />}
            onClick={handleProfileClick}
            // ❌ PROBLEMA: No dropdown menu con Profile, Orders, Logout
          >
            Profile
          </Button>
        ) : (
          <Button
            type="primary"
            onClick={handleLoginClick}
            // ❌ PROBLEMA: No loading state durante login
          >
            Login
          </Button>
        )}
      </Flex>
    </Header>
  );
};

// ❌ PROBLEMA: No export con React.memo para optimization
export default AppHeader;
