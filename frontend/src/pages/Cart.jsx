import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

function Cart() {
  const [cart, setCart] = useState({
    items: [],
    total_amount: 0,
  });

  const fetchCart = async () => {
    try {
      const response = await api.get("/cart/");
      setCart(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const updateQuantity = async (productId, quantity) => {
    if (quantity <= 0) {
      return;
    }

    try {
      await api.put(`/cart/items/${productId}?quantity=${quantity}`);
      fetchCart();
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to update quantity"
      );
    }
  };

  const removeItem = async (productId) => {
    try {
      await api.delete(`/cart/items/${productId}`);
      toast.success("Item removed from cart");
      fetchCart();
    } catch (error) {
      toast.error(
        error.response?.data?.detail || "Unable to remove item"
      );
    }
  };

  return (
    <div className="products-page">
      <h1>Shopping Cart</h1>

      <div className="cart-links">
        <Link className="cart-link" to="/products">
          Products
        </Link>

        <Link className="cart-link" to="/orders">
          My Orders
        </Link>
      </div>

      {cart.items.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div className="products-grid">
          {cart.items.map((item) => (
            <div className="product-card" key={item.product_id}>
              <h3>{item.product_name}</h3>

              <p>Price: ${item.price}</p>

              <p>Subtotal: ${item.subtotal}</p>

              <div className="quantity-controls">
                <button
                  className="quantity-button"
                  onClick={() =>
                    updateQuantity(
                      item.product_id,
                      item.quantity - 1
                    )
                  }
                >
                  -
                </button>

                <span className="quantity-number">
                  {item.quantity}
                </span>

                <button
                  className="quantity-button"
                  onClick={() =>
                    updateQuantity(
                      item.product_id,
                      item.quantity + 1
                    )
                  }
                >
                  +
                </button>
              </div>

              <button
                className="remove-button"
                onClick={() => removeItem(item.product_id)}
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="cart-total-container">
        <h2 className="cart-total">
          Total: ${cart.total_amount}
        </h2>
      </div>
    </div>
  );
}

export default Cart;