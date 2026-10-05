import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

function Orders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get("/orders/");
        setOrders(response.data.items);
      } catch (error) {
        console.log(error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="products-page">
      <h1>My Orders</h1>

      <div className="cart-links">
        <Link className="cart-link" to="/products">
          Products
        </Link>

        <Link className="cart-link" to="/cart">
          Cart
        </Link>
      </div>

      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <div className="products-grid">
          {orders.map((order) => (
            <div className="product-card" key={order.id}>
              <h3>Order #{order.id}</h3>

              <p>Status: {order.payment_status}</p>

              <p>Total: ${order.total_amount}</p>

              {order.items.map((item) => (
                <div key={item.product_id}>
                  <p>
                    {item.product_name} × {item.quantity}
                  </p>
                </div>
              ))}

              <div className="checkout-button">
                <button
                  onClick={async () => {
                    try {
                      const response = await api.post(
                        `/orders/${order.id}/checkout`
                      );

                      window.location.href =
                        response.data.checkout_url;
                    } catch (error) {
                    
                        toast.error(
                       error.response?.data?.detail || "Checkout failed"
                     );
                    }
                  }}
                >
                  Checkout
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Orders;