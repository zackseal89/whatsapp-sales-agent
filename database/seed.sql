-- Sample data for testing the WhatsApp AI Sales Agent

-- Sample Products
INSERT INTO products (sku, name, description, category, price, stock_quantity, image_urls, tags) VALUES
('TSHIRT-001', 'Classic White T-Shirt', 'Comfortable cotton t-shirt perfect for everyday wear', 'Clothing', 29.99, 150, ARRAY['https://example.com/images/tshirt-white.jpg'], ARRAY['casual', 'cotton', 'unisex']),
('JEANS-001', 'Blue Denim Jeans', 'Classic fit denim jeans with modern styling', 'Clothing', 79.99, 80, ARRAY['https://example.com/images/jeans-blue.jpg'], ARRAY['denim', 'casual']),
('PHONE-001', 'Smartphone XYZ', 'Latest smartphone with advanced camera and long battery life', 'Electronics', 699.99, 50, ARRAY['https://example.com/images/phone-xyz.jpg'], ARRAY['smartphone', 'electronics', 'tech']),
('LAPTOP-001', 'Laptop Pro 15"', 'Powerful laptop for work and entertainment', 'Electronics', 1299.99, 30, ARRAY['https://example.com/images/laptop-pro.jpg'], ARRAY['laptop', 'computer', 'work']),
('SHOES-001', 'Running Shoes', 'Lightweight running shoes with superior cushioning', 'Footwear', 119.99, 100, ARRAY['https://example.com/images/shoes-running.jpg'], ARRAY['sports', 'running', 'athletic']),
('HEADPHONES-001', 'Wireless Headphones', 'Noise-cancelling wireless headphones with 30hr battery', 'Electronics', 249.99, 75, ARRAY['https://example.com/images/headphones-wireless.jpg'], ARRAY['audio', 'wireless', 'music']),
('WATCH-001', 'Smart Watch', 'Fitness tracking smart watch with heart rate monitor', 'Electronics', 299.99, 60, ARRAY['https://example.com/images/watch-smart.jpg'], ARRAY['smartwatch', 'fitness', 'wearable']),
('BAG-001', 'Leather Backpack', 'Premium leather backpack with laptop compartment', 'Accessories', 159.99, 40, ARRAY['https://example.com/images/bag-leather.jpg'], ARRAY['backpack', 'leather', 'travel']),
('HOODIE-001', 'Zip-Up Hoodie', 'Comfortable zip-up hoodie with fleece lining', 'Clothing', 59.99, 120, ARRAY['https://example.com/images/hoodie-zip.jpg'], ARRAY['casual', 'warm', 'winter']),
('SUNGLASSES-001', 'Polarized Sunglasses', 'UV protection polarized sunglasses with stylish frames', 'Accessories', 89.99, 90, ARRAY['https://example.com/images/sunglasses-polarized.jpg'], ARRAY['sunglasses', 'eyewear', 'summer']);

-- Sample Admin User
INSERT INTO admin_users (email, name, role, permissions) VALUES
('admin@example.com', 'Admin User', 'owner', '{"all": true}'::jsonb),
('manager@example.com', 'Store Manager', 'manager', '{"view_orders": true, "manage_products": true}'::jsonb);

-- Sample Customers (for testing)
INSERT INTO customers (whatsapp_number, name, email, phone_country_code, preferred_language) VALUES
('+254712345678', 'John Doe', 'john@example.com', '+254', 'en'),
('+254723456789', 'Jane Smith', 'jane@example.com', '+254', 'en'),
('+254734567890', 'Michael Johnson', 'michael@example.com', '+254', 'en');

-- Notes:
-- 1. Replace image URLs with actual URLs when products are added
-- 2. Update admin email addresses with real ones
-- 3. Customer phone numbers are examples - real customers will be created via WhatsApp interactions
