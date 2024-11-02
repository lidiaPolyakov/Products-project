import React from 'react';
import './style/product.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';

const Product = ({ product, onEdit, onDelete }) => {
  return (
    <div className="product-item">
      <div className="product-actions">
        <button onClick={() => onEdit(product)}>
          <FontAwesomeIcon icon={faEdit} />
        </button>
        <button onClick={() => onDelete(product._id)}>
          <FontAwesomeIcon icon={faTrashAlt} />
        </button>
      </div>
      <h3>Product Name: {product.productName}</h3>
      <p>Number: {product.number}</p>
      <p>SKU: {product.productSKU}</p>
      <p>Description: {product.productDescription}</p>
      <p>Type: {product.productType}</p>
      {/* <p>Marketing Date: {product.productMarketingDate}</p> */}
      <p>Marketing Date: {new Date(product.productMarketingDate).toLocaleDateString()}</p>
    </div>
  );
};

export default Product;
