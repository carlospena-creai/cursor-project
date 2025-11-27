import React from "react";
import { useSearchParams } from "react-router-dom";
import { Typography } from "antd";
import { ProductsList } from "../components/ProductsList";
import type { ProductsFilters } from "../types/product.types";

const { Title } = Typography;

const SearchResultsPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get("q") || "";
  const category = searchParams.get("category") || undefined;

  const filters: ProductsFilters = {};
  if (searchQuery) {
    filters.search = searchQuery;
  }
  if (category) {
    filters.category = category;
  }

  const getPageTitle = () => {
    if (searchQuery && category) {
      return `Search results for "${searchQuery}" in ${category}`;
    }
    if (searchQuery) {
      return `Search results for "${searchQuery}"`;
    }
    if (category) {
      return `Products in ${category}`;
    }
    return "All Products";
  };

  return (
    <div>
      <Title level={2} style={{ marginBottom: "24px" }}>
        {getPageTitle()}
      </Title>
      <ProductsList initialFilters={filters} title="" />
    </div>
  );
};

export default SearchResultsPage;
