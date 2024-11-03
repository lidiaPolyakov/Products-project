import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './style/form.css';

// Using the useState and useEffect hooks from React to manage the form state and handle form submission. 
const Form = ({ product }) => {
  const [formData, setFormData] = useState(product);
  const [productName, setProductName] = useState('');
  const [productSKU, setProductSKU] = useState('');
  const [productDescription, setProductDescription] = useState('');
  const [productType, setProductType] = useState('vegetable');
  const [productMarketingDate, setProductMarketingDate] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Initialize form fields when the product prop changes
    setFormData(product || {});
    setProductName(product?.productName || '');
    setProductSKU(product?.productSKU || '');
    setProductDescription(product?.productDescription || '');
    setProductType(product?.productType || 'vegetable');
    setProductMarketingDate(
      product?.productMarketingDate
        ? new Date(product.productMarketingDate).toISOString().slice(0, 10) //'YYYY-MM-DD' When product.productMarketingDate exists:
        : (() => {
          const date = new Date();
          date.setDate(date.getDate() - 7);
          return date.toISOString().slice(0, 10); // 'YYYY-MM-DD' When product.productMarketingDate does not exist
        })()
    );
  }, [product]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const updatedFormData = {
      productName,
      productSKU,
      productDescription,
      productType,
      productMarketingDate,
    };

    try {
      if (product?._id) {
        // Update existing product
        const response = await axios.put(`http://localhost:5000/product/${product._id}`, updatedFormData);
        setMessage(response.data.message);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        window.location.reload();
      } else {
        // Create new product
        const response = await axios.post('http://localhost:5000/product', updatedFormData);
        setMessage(response.data.message);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        window.location.reload();
      }
    } catch (error) {
      if (error.response.status === 409) {
        setMessage('SKU already exists. Please use a unique SKU.');
      } else {
        setMessage('Product submission failed. Please try again.');
      }
    }
  };

  const handleClose = () => {
    window.location.reload();
  };

  if (!formData) return null;
  return (
    <div className="product-modal">
      <div className="product-form">
        <h2>{formData.productName ? formData.productName : 'New Product'}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Product Name:
            <input
              type="text"
              name="productName"
              value={productName}
              maxLength="50"
              required
              onChange={(e) => setProductName(e.target.value)}
            />
          </label>
          <label>
            SKU:
            <input
              type="number"
              name="productSKU"
              value={productSKU}
              min="0"
              required
              onChange={(e) => setProductSKU(e.target.value)}
            />
          </label>
          <label>
            Description:
            <textarea
              name="productDescription"
              value={productDescription}
              onChange={(e) => setProductDescription(e.target.value)}
            ></textarea>
          </label>
          <label>
            Type:
            <select
              name="productType"
              value={productType}
              required
              onChange={(e) => setProductType(e.target.value)}
            >
              <option value="vegetable">Vegetable</option>
              <option value="fruit">Fruit</option>
              <option value="field crops">Field Crops</option>
            </select>
          </label>
          <label>
            Marketing Date:
            <input
              type="date"
              name="productMarketingDate"
              value={productMarketingDate}
              onChange={(e) => setProductMarketingDate(e.target.value)}
            />
          </label>
          <button type="submit">Save</button>
          <button type="button" onClick={handleClose}>Close</button>
          <p>{message}</p>
        </form>
      </div>
    </div>
  );
};

export default Form;
