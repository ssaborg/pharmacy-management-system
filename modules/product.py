# modules/product.py - Product Management Module
# PLACEMENT: pharmacy-management-system/modules/product.py
# Handles all product/item related database operations

from database import DatabaseManager

class ProductManager:
    """
    Manages product/item operations
    Provides methods for CRUD operations on products
    """
    
    def __init__(self):
        """Initialize product manager with database connection"""
        self.db = DatabaseManager()
        self.db.connect()
    
    def add_product(self, product_name, product_code, category, unit, purchase_price, selling_price, minimum_stock):
        """
        Add a new product to database
        Returns: True if successful, False otherwise
        """
        query = """
        INSERT INTO products (product_name, product_code, category, unit, purchase_price, selling_price, minimum_stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (product_name, product_code, category, unit, purchase_price, selling_price, minimum_stock)
        return self.db.execute_query(query, params)
    
    def get_all_products(self):
        """Get all products from database"""
        query = "SELECT * FROM products ORDER BY product_name"
        return self.db.fetch_all(query)
    
    def get_product_by_id(self, product_id):
        """Get product details by product ID"""
        query = "SELECT * FROM products WHERE product_id = ?"
        return self.db.fetch_one(query, (product_id,))
    
    def get_product_by_code(self, product_code):
        """Get product details by product code"""
        query = "SELECT * FROM products WHERE product_code = ?"
        return self.db.fetch_one(query, (product_code,))
    
    def update_product(self, product_id, product_name, product_code, category, unit, purchase_price, selling_price, minimum_stock):
        """Update product details"""
        query = """
        UPDATE products 
        SET product_name = ?, product_code = ?, category = ?, unit = ?, 
            purchase_price = ?, selling_price = ?, minimum_stock = ?, updated_at = CURRENT_TIMESTAMP
        WHERE product_id = ?
        """
        params = (product_name, product_code, category, unit, purchase_price, selling_price, minimum_stock, product_id)
        return self.db.execute_query(query, params)
    
    def delete_product(self, product_id):
        """Delete product by ID"""
        query = "DELETE FROM products WHERE product_id = ?"
        return self.db.execute_query(query, (product_id,))
    
    def update_stock(self, product_id, quantity_change):
        """
        Update product stock (add or subtract)
        quantity_change: positive number to add, negative to subtract
        """
        query = """
        UPDATE products 
        SET current_stock = current_stock + ?, updated_at = CURRENT_TIMESTAMP
        WHERE product_id = ?
        """
        return self.db.execute_query(query, (quantity_change, product_id))
    
    def get_low_stock_products(self):
        """Get products that are below minimum stock level"""
        query = "SELECT * FROM products WHERE current_stock <= minimum_stock"
        return self.db.fetch_all(query)
    
    def product_exists(self, product_name, product_id=None):
        """Check if product name already exists"""
        if product_id:
            query = "SELECT product_id FROM products WHERE product_name = ? AND product_id != ?"
            result = self.db.fetch_one(query, (product_name, product_id))
        else:
            query = "SELECT product_id FROM products WHERE product_name = ?"
            result = self.db.fetch_one(query, (product_name,))
        return result is not None
    
    def __del__(self):
        """Cleanup: close database connection"""
        self.db.disconnect()
