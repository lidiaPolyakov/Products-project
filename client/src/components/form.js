import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './style/form.css';


const Form = ({ product }) => {
  const [formData, setFormData] = useState(product);
  const [title, settitle] = useState('');
  const [description, setdescription] = useState('');
  const [date, setdate] = useState('');
  const [price, setprice] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Set form data and other fields when the product prop changes
    setFormData(product || {});
    settitle(product?.title || '');
    setdescription(product?.description || '');
    setdate(product?.date || '');
    setprice(product?.price || '');
  }, [product]);

  
  const handleSubmit = async (e) => {
    e.preventDefault();  
    // Update formData with the current input values
    const updatedFormData = {
      title,
      description,
      date,
      price,
    };
    try {
      if (product?._id) {
        const response = await axios.put(`http://localhost:5000/product/${product._id}`, updatedFormData);
        console.log("im in edit:", product._id);
        setMessage(response.data.message);
        await new Promise(resolve => setTimeout(resolve, 1000));
        window.location.reload();
      } else {
        const response = await axios.post('http://localhost:5000/product', updatedFormData);
        console.log("im in create:", product._id);
        setMessage(response.data.message);
        await new Promise(resolve => setTimeout(resolve, 1000));
        window.location.reload();
      }
    } catch (error) {
      setMessage('product failed. Please try again.'); 
    }
  };
  
  const handleClose = () => {
    window.location.reload();
  };
  
  if (!formData) return null;
  return (
    <div className="product-modal">
      <div className="product-form" value={formData} onChange={(e) => setFormData(e.target.value)}>
        <h2>{formData.title ? formData.title : "New Product"}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Title:
            <input type="text" name="title" value={title} onChange={(e) => settitle(e.target.value)} />
          </label>
          <label>
            Description:
            <textarea name="description" value={description} onChange={(e) => setdescription(e.target.value)}></textarea>
          </label>
          <label>
            Date:
            <input type="date" name="date" value={date} onChange={(e) => setdate(e.target.value)} />
          </label>
          <label>
            Price:
            <input type="text" name="price" value={price} onChange={(e) => setprice(e.target.value)} />
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