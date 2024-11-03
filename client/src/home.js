import React, { useState, useEffect } from 'react';
import axios from 'axios';

import Navbar from './components/navbar';
import Header from './components/header';
import Form from './components/form';
import Product from './components/product';
import './style/home.css';

const Home = () => {
  const [activeProduct, setActiveProduct] = useState(null);
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const handleAddProduct = () => {
    setActiveProduct({ FormData:"", productName: "", productSKU: "", productDescription: "", productType: "", productMarketingDate: "" });
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/product');
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleEditProduct = (product) => {
    setActiveProduct(product); 
  };

  const handleDeleteProduct = async (productId) => {
    console.log("Deleting product with ID:", productId);
    const updatedProducts = products.filter((product) => product._id !== productId);
    setProducts(updatedProducts);
    try {
      await axios.delete(`http://localhost:5000/product/${productId}`);
    } catch (error) {
      console.error("Failed to delete product:", error);
      setProducts(products);
    }
  };

  const searchProductsByName = async (searchTerm = "") => {
    try {
      const response = await axios.get(`http://localhost:5000/product?productName=${searchTerm}`);
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    searchProductsByName(searchTerm);
  }, [searchTerm]);

  return (
    <div className={`home ${activeProduct ? 'blurred' : ''}`}>
      <Navbar />
      <div className="main-content">
        <Header />
        <section className="products">
          <h2>Our Products</h2>
          <div className="search-and-add">
            <input
              type="text"
              placeholder="Search products by name..."
              className="search-input"
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="add-product-button" onClick={handleAddProduct}>+</button>
          <div className="product-list">
            {products.map((product) => (
              <Product
                key={product._id}
                product={product}
                onEdit={handleEditProduct}
                onDelete={handleDeleteProduct}
              />
            ))}
          </div>
        </section>
        {/* <Buffer /> */}
      </div>
      {activeProduct && (
        <Form product={activeProduct} />
      )}
    </div>
  );
};

export default Home;
