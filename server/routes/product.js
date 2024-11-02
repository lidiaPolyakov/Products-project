const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

router.post('/', async (req, res) => {
  const { title, description, date, price } = req.body;
  let product = new Product({title, description, date, price});
  await product.save();
  res.json({ message: 'Saved successful!' });
  
});


router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { title, description, date, price } = req.body;
  try {
    const updatedProduct = await Product.findByIdAndUpdate(
      id,
      { title, description, date, price },
      { new: true }
    );
    res.json({ message: 'Saved successful!' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get products (optionally filtered by title)
router.get('/', async (req, res) => {
  const { title } = req.query;
  try {
    const products = title
      ? await Product.find({ title: { $regex: title, $options: 'i' } })
      : await Product.find();
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});


// Delete a product
router.delete('/:id', async (req, res) => {

  const { id } = req.params;
  try {
    const deletedProduct = await Product.findByIdAndDelete(id);
    if (!deletedProduct) {
      return res.status(404).json({ message: 'Product not found' });
    }
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;















// const express = require('express');
// const router = express.Router();
// const Ticket = require('../models/Ticket');

// // Create a new ticket
// router.post('/', async (req, res) => {
//   const { title, description, date, price } = req.body;
//   try {
//     const newTicket = new Ticket({ title, description, date, price });
//     await newTicket.save();
//     res.status(201).json(newTicket);
//   } catch (error) {
//     res.status(400).json({ error: error.message });
//   }
// });



// // Update a ticket
// router.put('/:id', async (req, res) => {
//   const { id } = req.params;
//   const { title, description, date, price } = req.body;
//   try {
//     const updatedTicket = await Ticket.findByIdAndUpdate(id, { title, description, date, price }, { new: true });
//     res.status(200).json(updatedTicket);
//   } catch (error) {
//     res.status(400).json({ error: error.message });
//   }
// });

// // Delete a ticket
// router.delete('/:id', async (req, res) => {
//   const { id } = req.params;
//   try {
//     await Ticket.findByIdAndDelete(id);
//     res.status(200).json({ message: 'Ticket deleted successfully' });
//   } catch (error) {
//     res.status(400).json({ error: error.message });
//   }
// });

// module.exports = router;
