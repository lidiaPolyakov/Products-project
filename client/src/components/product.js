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
      <h3>{product.title}</h3>
      <p>{product.description}</p>
      <p>Date: {product.date}</p>
      <p>Price: ${product.price}</p>
    </div>
  );
};

export default Product;
