const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

router.post('/', async (req, res) => {
  const { productName, productSKU, productDescription, productType, productMarketingDate } = req.body;
  let product = new Product({ productName, productSKU, productDescription, productType, productMarketingDate });
  // Check if the product SKU already exists
  const existingProduct = await Product.findOne({ productSKU });
  if (existingProduct) {
    return res.status(409).json({ error: 'Duplicate SKU detected' }); // Use HTTP 409 Conflict status  
  }
  try {
    await product.save();
    res.json({ message: 'Product saved successfully!' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { productName, productSKU, productDescription, productType, productMarketingDate } = req.body;

  try {
    const existingProduct = await Product.findOne({ productSKU, _id: { $ne: id } });
    if (existingProduct) {
      return res.status(409).json({ error: 'Duplicate SKU detected' });
    }

    await Product.findByIdAndUpdate(
      id,
      { productName, productSKU, productDescription, productType, productMarketingDate },
      { new: true }
    );
    res.json({ message: 'Product updated successfully!' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.get('/', async (req, res) => {
  const { productName } = req.query;
  try {
    const products = productName
      ? await Product.find({ productName: { $regex: productName, $options: 'i' } })
      : await Product.find();
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});


router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const deletedProduct = await Product.findByIdAndDelete(id);
    if (!deletedProduct) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json({ message: 'Product deleted successfully!' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;





