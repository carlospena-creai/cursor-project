/**
 * Cart Context
 *
 * Context API para manejar el estado global del carrito.
 * Proporciona funciones para agregar, remover y actualizar items.
 */
import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import type { CartItem } from "../types/order.types";
import type { Product } from "../../Products/types/product.types";

interface CartContextType {
  items: CartItem[];
  addItem: (product: Product, quantity?: number) => void;
  removeItem: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clearCart: () => void;
  getTotal: () => number;
  getItemCount: () => number;
  isInCart: (productId: number) => boolean;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

const CART_STORAGE_KEY = "ecommerce_cart";

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [items, setItems] = useState<CartItem[]>(() => {
    // Cargar carrito desde localStorage al inicializar
    try {
      const savedCart = localStorage.getItem(CART_STORAGE_KEY);
      return savedCart ? JSON.parse(savedCart) : [];
    } catch (error) {
      console.error("Error loading cart from localStorage:", error);
      return [];
    }
  });

  // Guardar carrito en localStorage cuando cambie
  useEffect(() => {
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
    } catch (error) {
      console.error("Error saving cart to localStorage:", error);
    }
  }, [items]);

  const addItem = useCallback((product: Product, quantity: number = 1) => {
    setItems((prevItems) => {
      const existingItem = prevItems.find(
        (item) => item.productId === product.id
      );

      if (existingItem) {
        // Si el producto ya está en el carrito, actualizar cantidad
        const newQuantity = existingItem.quantity + quantity;
        if (newQuantity > product.stock) {
          // No exceder el stock disponible
          return prevItems;
        }
        return prevItems.map((item) =>
          item.productId === product.id
            ? {
                ...item,
                quantity: newQuantity,
                subtotal: product.price * newQuantity,
              }
            : item
        );
      } else {
        // Agregar nuevo item al carrito
        if (quantity > product.stock) {
          return prevItems;
        }
        return [
          ...prevItems,
          {
            productId: product.id,
            productName: product.name,
            quantity,
            unitPrice: product.price,
            subtotal: product.price * quantity,
          },
        ];
      }
    });
  }, []);

  const removeItem = useCallback((productId: number) => {
    setItems((prevItems) =>
      prevItems.filter((item) => item.productId !== productId)
    );
  }, []);

  const updateQuantity = useCallback(
    (productId: number, quantity: number) => {
      if (quantity <= 0) {
        removeItem(productId);
        return;
      }

      setItems((prevItems) =>
        prevItems.map((item) => {
          if (item.productId === productId) {
            return {
              ...item,
              quantity,
              subtotal: item.unitPrice * quantity,
            };
          }
          return item;
        })
      );
    },
    [removeItem]
  );

  const clearCart = useCallback(() => {
    setItems([]);
  }, []);

  const getTotal = useCallback(() => {
    return items.reduce((total, item) => total + item.subtotal, 0);
  }, [items]);

  const getItemCount = useCallback(() => {
    return items.reduce((count, item) => count + item.quantity, 0);
  }, [items]);

  const isInCart = useCallback(
    (productId: number) => {
      return items.some((item) => item.productId === productId);
    },
    [items]
  );

  const value: CartContextType = {
    items,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    getTotal,
    getItemCount,
    isInCart,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = (): CartContextType => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};
