const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors()); // Enable CORS
app.use(bodyParser.json());

// Serve static files from the "public" directory
app.use(express.static('public'));

// Initialize SQLite database
const db = new sqlite3.Database(':memory:');

// Create Menu Table
db.serialize(() => {
  db.run(`CREATE TABLE menu (
    id INTEGER PRIMARY KEY,
    name TEXT,
    image TEXT,
    price TEXT,
    quantity TEXT
  )`);

  const stmt = db.prepare("INSERT INTO menu (name, image, price, quantity) VALUES (?, ?, ?, ?)");

  const menuItems = [
    ["Klepon Cheesecake", "/assets/images/menu_1.webp", "$6.99", "1 slice"],
    ["Rendang Beef Burgers", "/assets/images/menu_2.webp", "$12.99", "1 burger"],
    ["Mie Goreng Stir-Fry", "/assets/images/menu_3.webp", "$9.99", "1 bowl"],
    ["Indonesian Meatball Soup", "/assets/images/menu_4.webp", "$7.99", "1 bowl"],
    ["Ayam Bakar Teriyaki", "/assets/images/menu_5.webp", "$11.99", "2 pieces"],
    ["Sambal Chicken Wings", "/assets/images/menu_6.webp", "$8.99", "6 pieces"],
    ["Nasi Uduk with Grilled Fish", "/assets/images/menu_7.webp", "$10.99", "1 plate"],
    ["Katsu Curry with Nasi", "/assets/images/menu_8.webp", "$13.99", "1 plate"],
    ["Nasi Campur Bowl", "/assets/images/menu_9.webp", "$9.99", "1 bowl"],
    ["Balinese Spiced Veggie Pizza", "/assets/images/menu_10.webp", "$14.99", "1 pizza"]
  ];

  menuItems.forEach(item => {
    stmt.run(item[0], item[1], item[2], item[3]);
  });

  stmt.finalize();
});

// Endpoint to get menu items
app.get('/api/menu', (req, res) => {
  console.log('Request received for /api/menu');
  db.all("SELECT * FROM menu", [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    console.log('Data retrieved from database:', rows);
    res.json({
      data: rows
    });
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});