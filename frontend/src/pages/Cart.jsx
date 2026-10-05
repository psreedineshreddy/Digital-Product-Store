import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";

function Cart() {
  const [cart, setCart] = useState({
    items: [],
    total_amount: 0,
  });

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await api.get("/cart/");
        setCart(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchCart();
  }, []);

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

              <p>Quantity: {item.quantity}</p>

              <p>Subtotal: ${item.subtotal}</p>
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