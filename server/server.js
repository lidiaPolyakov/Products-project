// server.js
require('dotenv').config()
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
const mongoUsername = process.env.MONGO_USERNAME;
const mongoPassword = process.env.MONGO_PASSWORD;
const uri = `mongodb+srv://${mongoUsername}:${mongoPassword}@lidiaapp.fsexp.mongodb.net/?retryWrites=true&w=majority&appName=LidiaApp`;
const clientOptions = {
  serverApi: { version: '1', strict: true, deprecationErrors: true}
};
async function run() {
  try {
    // Create a Mongoose client with a MongoClientOptions object to set the Stable API version
    await mongoose.connect(uri, clientOptions);
    await mongoose.connection.db.admin().command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
  }
}
run().catch(console.dir);



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
