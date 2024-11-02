// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const User = require('./models/user');
const Product = require('./models/Product');
const productRoutes = require('./routes/product');

const app = express();
const port = 5000;
const jwtSecret = 'your_jwt_secret';

mongoose.connect('mongodb://127.0.0.1:27017/loginapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

app.use(cors());
app.use(express.json());
app.use('/product', productRoutes);


app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(400).json({ message: 'Invalid email or password.' });
  }
  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) {
    return res.status(400).json({ message: 'Invalid email or password.' });
  }
  const token = jwt.sign({ id: user._id }, jwtSecret, { expiresIn: '1h' });
  res.json({ token, message: 'Login successful!' });
});

app.post('/signup', async (req, res) => {
  const { email, password } = req.body;
  try {
    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ message: 'User already exists.' });
    }
    user = new User({ email, password });
    await user.save();
    res.json({ message: 'Signup successful!' });
  } catch (error) {
    console.error(error.message);
    res.status(500).send('Server Error');
  }
});



app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
