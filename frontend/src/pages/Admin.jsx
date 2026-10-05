import { useEffect, useState } from "react";
import api from "../api/axios";

function Admin() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get("/orders/admin/stats");
        setStats(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="products-page">
      <h1>Admin Dashboard</h1>

      {!stats ? (
        <p>Loading...</p>
      ) : (
        <div className="products-grid">
          <div className="product-card">
            <h3>Total Users</h3>
            <p>{stats.total_users}</p>
          </div>

          <div className="product-card">
            <h3>Total Products</h3>
            <p>{stats.total_products}</p>
          </div>

          <div className="product-card">
            <h3>Total Orders</h3>
            <p>{stats.total_orders}</p>
          </div>

          <div className="product-card">
            <h3>Total Revenue</h3>
            <p>${stats.total_revenue}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Admin;