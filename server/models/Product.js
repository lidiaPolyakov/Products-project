const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  // number: {
  //   type: Number,
  //   default: function() {
  //     return autoIncrement++;
  //   },
  //   unique: true,
  //   immutable: true,
  // },
  productName: {
    type: String,
    required: true,
    maxlength: 50,
  },
  productSKU: {
    type: Number,
    required: true,
    unique: true,
    min: 0,
  },
  productDescription: {
    type: String,
  },
  productType: {
    type: String,
    required: true,
    enum: ['vegetable', 'fruit', 'field crops'],
  },
  productMarketingDate: {
    type: Date,
    default: function() {
      const today = new Date();
      today.setDate(today.getDate() - 7);
      return today;
    },
  },
});

module.exports = mongoose.model('Product', productSchema);
