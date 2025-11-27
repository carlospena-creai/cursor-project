/**
 * Products Feature - Barrel Export
 *
 * Feature-based architecture: exporta componentes y hooks públicos del feature.
 */
export { ProductsList } from "./components/ProductsList";
export { ProductCard } from "./components/ProductCard";
export { useProducts } from "./hooks/useProducts";
export type {
  Product,
  ProductsFilters,
  ProductsResponse,
} from "./types/product.types";
export { default as ProductsPage } from "./pages/ProductsPage";
