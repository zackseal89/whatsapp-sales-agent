-- =====================================================
-- WhatsApp AI Sales Agent - Database Schema
-- =====================================================
-- This schema supports the complete workflow:
-- - Customer management
-- - Product catalog
-- - Conversations & messages
-- - Shopping cart & orders
-- - Analytics tracking
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search

-- =====================================================
-- CUSTOMERS TABLE
-- =====================================================
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  whatsapp_number VARCHAR(20) UNIQUE NOT NULL,
  name VARCHAR(255),
  email VARCHAR(255),
  phone_country_code VARCHAR(5),
  preferred_language VARCHAR(10) DEFAULT 'en',
  customer_since TIMESTAMPTZ DEFAULT NOW(),
  total_orders INTEGER DEFAULT 0,
  total_spent DECIMAL(12, 2) DEFAULT 0.00,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for customers
CREATE INDEX idx_customers_whatsapp ON customers(whatsapp_number);
CREATE INDEX idx_customers_email ON customers(email) WHERE email IS NOT NULL;
CREATE INDEX idx_customers_created_at ON customers(created_at);

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- PRODUCTS TABLE
-- =====================================================
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(500) NOT NULL,
  description TEXT,
  category VARCHAR(100),
  subcategory VARCHAR(100),
  price DECIMAL(12, 2) NOT NULL,
  compare_at_price DECIMAL(12, 2),
  currency VARCHAR(3) DEFAULT 'USD',
  stock_quantity INTEGER DEFAULT 0,
  low_stock_threshold INTEGER DEFAULT 5,
  image_urls TEXT[],
  tags TEXT[],
  is_active BOOLEAN DEFAULT true,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for products
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
CREATE INDEX idx_products_description_trgm ON products USING gin(description gin_trgm_ops);
CREATE INDEX idx_products_tags ON products USING gin(tags);

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- CONVERSATIONS TABLE
-- =====================================================
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
  whatsapp_number VARCHAR(20) NOT NULL,
  status VARCHAR(50) DEFAULT 'active', -- active, resolved, escalated, closed
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  last_message_at TIMESTAMPTZ DEFAULT NOW(),
  message_count INTEGER DEFAULT 0,
  agent_handled BOOLEAN DEFAULT true, -- false if human took over
  sentiment_score DECIMAL(3, 2), -- -1.0 to 1.0
  resolution_type VARCHAR(100), -- sale, inquiry, support, abandoned
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for conversations
CREATE INDEX idx_conversations_customer ON conversations(customer_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_started ON conversations(started_at);
CREATE INDEX idx_conversations_last_message ON conversations(last_message_at);
CREATE INDEX idx_conversations_whatsapp ON conversations(whatsapp_number);

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- MESSAGES TABLE
-- =====================================================
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  whatsapp_message_id VARCHAR(255) UNIQUE,
  direction VARCHAR(20) NOT NULL, -- inbound, outbound
  sender_type VARCHAR(20) NOT NULL, -- customer, agent, system
  content_type VARCHAR(50) DEFAULT 'text', -- text, image, audio, video, document
  message_text TEXT,
  media_url TEXT,
  media_mime_type VARCHAR(100),
  intent VARCHAR(100), -- browse, inquire, order, support, etc.
  agent_name VARCHAR(100), -- which specialized agent handled this
  is_automated BOOLEAN DEFAULT true,
  confidence_score DECIMAL(3, 2),
  metadata JSONB,
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  delivered_at TIMESTAMPTZ,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for messages
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);
CREATE INDEX idx_messages_direction ON messages(direction);
CREATE INDEX idx_messages_whatsapp_id ON messages(whatsapp_message_id);
CREATE INDEX idx_messages_text_trgm ON messages USING gin(message_text gin_trgm_ops);

-- =====================================================
-- SESSIONS TABLE (for ADK context retention)
-- =====================================================
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
  session_data JSONB, -- ADK session state
  last_active_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for sessions
CREATE INDEX idx_sessions_conversation ON sessions(conversation_id);
CREATE INDEX idx_sessions_customer ON sessions(customer_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- =====================================================
-- CART ITEMS TABLE
-- =====================================================
CREATE TABLE cart_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 1,
  price_at_addition DECIMAL(12, 2),
  added_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for cart
CREATE INDEX idx_cart_customer ON cart_items(customer_id);
CREATE INDEX idx_cart_product ON cart_items(product_id);

CREATE TRIGGER update_cart_items_updated_at BEFORE UPDATE ON cart_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ORDERS TABLE
-- =====================================================
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number VARCHAR(50) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, processing, shipped, delivered, cancelled
  subtotal DECIMAL(12, 2) NOT NULL,
  tax DECIMAL(12, 2) DEFAULT 0.00,
  shipping_cost DECIMAL(12, 2) DEFAULT 0.00,
  discount DECIMAL(12, 2) DEFAULT 0.00,
  total DECIMAL(12, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'USD',
  payment_status VARCHAR(50) DEFAULT 'unpaid', -- unpaid, pending, paid, failed, refunded
  payment_method VARCHAR(50),
  payment_reference VARCHAR(255),
  shipping_address JSONB,
  notes TEXT,
  metadata JSONB,
  placed_at TIMESTAMPTZ DEFAULT NOW(),
  confirmed_at TIMESTAMPTZ,
  shipped_at TIMESTAMPTZ,
  delivered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for orders
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_placed_at ON orders(placed_at);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ORDER ITEMS TABLE
-- =====================================================
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  product_snapshot JSONB, -- product details at time of order
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(12, 2) NOT NULL,
  subtotal DECIMAL(12, 2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for order items
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- =====================================================
-- ANALYTICS EVENTS TABLE
-- =====================================================
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type VARCHAR(100) NOT NULL, -- message_sent, order_placed, cart_abandoned, etc.
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  event_data JSONB,
  occurred_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for analytics
CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_occurred_at ON analytics_events(occurred_at);
CREATE INDEX idx_analytics_events_customer ON analytics_events(customer_id);

-- =====================================================
-- ADMIN USERS TABLE (for dashboard)
-- =====================================================
CREATE TABLE admin_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  role VARCHAR(50) DEFAULT 'admin', -- owner, admin, manager, support
  permissions JSONB,
  is_active BOOLEAN DEFAULT true,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for admin users
CREATE INDEX idx_admin_users_email ON admin_users(email);
CREATE INDEX idx_admin_users_role ON admin_users(role);

CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE cart_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- Admin policies (allow full access for authenticated admins)
CREATE POLICY "Admins can view all customers"
  ON customers FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.id = auth.uid()
      AND admin_users.is_active = true
    )
  );

CREATE POLICY "Admins can manage products"
  ON products FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.id = auth.uid()
      AND admin_users.is_active = true
    )
  );

CREATE POLICY "Admins can view all conversations"
  ON conversations FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.id = auth.uid()
      AND admin_users.is_active = true
    )
  );

CREATE POLICY "Admins can view all messages"
  ON messages FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.id = auth.uid()
      AND admin_users.is_active = true
    )
  );

CREATE POLICY "Admins can view all orders"
  ON orders FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.id = auth.uid()
      AND admin_users.is_active = true
    )
  );

-- Service role has full access (for backend agent)
CREATE POLICY "Service role can do everything on customers"
  ON customers FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on products"
  ON products FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on conversations"
  ON conversations FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on messages"
  ON messages FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on sessions"
  ON sessions FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on cart"
  ON cart_items FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on orders"
  ON orders FOR ALL
  TO service_role
  USING (true);

CREATE POLICY "Service role can do everything on analytics"
  ON analytics_events FOR ALL
  TO service_role
  USING (true);

-- =====================================================
-- UTILITY FUNCTIONS
-- =====================================================

-- Function to generate unique order number
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS VARCHAR AS $$
DECLARE
  new_order_number VARCHAR;
BEGIN
  new_order_number := 'ORD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
  RETURN new_order_number;
END;
$$ LANGUAGE plpgsql;

-- Function to update customer stats after order
CREATE OR REPLACE FUNCTION update_customer_stats()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'confirmed' AND OLD.status != 'confirmed' THEN
    UPDATE customers
    SET 
      total_orders = total_orders + 1,
      total_spent = total_spent + NEW.total
    WHERE id = NEW.customer_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_customer_stats
  AFTER UPDATE ON orders
  FOR EACH ROW
  EXECUTE FUNCTION update_customer_stats();

-- Function to update conversation message count
CREATE OR REPLACE FUNCTION update_conversation_message_count()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations
  SET 
    message_count = message_count + 1,
    last_message_at = NEW.sent_at
  WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_message_count
  AFTER INSERT ON messages
  FOR EACH ROW
  EXECUTE FUNCTION update_conversation_message_count();
