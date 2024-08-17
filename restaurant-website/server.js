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
    ["Cheesecake", "/assets/images/menu_1.webp", "$6.99", "21"],
    ["Beef Burgers", "/assets/images/menu_2.webp", "$12.99", "31"],
    ["Fried Noodle", "/assets/images/menu_3.webp", "$9.99", "11"],
    ["Meatball Soup", "/assets/images/menu_4.webp", "$7.99", "21"],
    ["Chicken Teriyaki", "/assets/images/menu_5.webp", "$11.99", "12"],
    ["Sambal Chicken Wings", "/assets/images/menu_6.webp", "$8.99", "16"],
    ["Grilled Fish", "/assets/images/menu_7.webp", "$10.99", "13"],
    ["Katsu Curry", "/assets/images/menu_8.webp", "$13.99", "11"],
    ["Mixed Rice Bowl", "/assets/images/menu_9.webp", "$9.99", "12"],
    ["Veggie Pizza", "/assets/images/menu_10.webp", "$14.99", "12"]
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

// Endpoint to handle voice order transcript
app.post('/api/voice-order', (req, res) => {
  const { transcript } = req.body;
  console.log('Received transcript:', transcript);

  // Here you can process the transcript further,
  // such as parsing the order, saving it to the database, etc.

  // For example, you could parse the transcript to match menu items and quantities
  // and save the parsed order to your SQLite database.

  res.status(200).json({ message: 'Transcript received successfully', transcript });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
