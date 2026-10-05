import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

function Products() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await api.get("/products/", {
          params: {
            search: search,
            page: page,
            limit: 10,
          },
        });

        setProducts(response.data.items);
      } catch (error) {
        console.log(error);
      }
    };

    fetchProducts();
  }, [search, page]);

  return (
    <div className="products-page">
      <h1>Digital Product Store</h1>

      <h2>Products</h2>

      <input
       className="search-input"
       type="text"
       placeholder="Search products..."
       value={search}
       onChange={(e) => {
        setSearch(e.target.value);
        setPage(1);
  }}
/>

      <div className="cart-links">
        <Link className="cart-link" to="/cart">
          View Cart
        </Link>

        <Link className="cart-link" to="/orders">
          My Orders
        </Link>
      </div>

      <div className="products-grid">
        {products.map((product) => (
          <div className="product-card" key={product.id}>
            <h3>{product.name}</h3>

            <p>{product.description}</p>

            <p className="product-price">
              ${product.price}
            </p>

            <button
              onClick={async () => {
                try {
                  await api.post("/cart/items", {
                    product_id: product.id,
                    quantity: 1,
                  });

                  toast.success("Added to cart");
                } catch (error) {
                  toast.error(
                    error.response?.data?.detail ||
                      "Failed to add to cart"
                  );
                }
              }}
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>

      <div className="pagination">
        <button
          onClick={() => setPage(page - 1)}
          disabled={page === 1}
        >
          Previous
        </button>

        <span>Page {page}</span>

        <button
          onClick={() => setPage(page + 1)}
          disabled={products.length < 10}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default Products;