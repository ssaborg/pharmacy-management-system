# database.py - Database Schema and Initialization
# PLACEMENT: Root directory of project (pharmacy-management-system/database.py)

import sqlite3
import os
from config import DATABASE_PATH

class DatabaseManager:
    """
    Manages all database operations for Pharmacy Management System
    Creates tables, initializes database, and provides connection management
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.db_path = DATABASE_PATH
        self.connection = None
    
    def connect(self):
        """Create connection to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            return self.connection
        except sqlite3.Error as e:
            print(f"Database Connection Error: {e}")
            return None
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=()):
        """
        Execute INSERT, UPDATE, DELETE queries
        Returns True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Query Execution Error: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query, params=()):
        """Fetch all records from SELECT query"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Fetch Error: {e}")
            return []
    
    def fetch_one(self, query, params=()):
        """Fetch single record from SELECT query"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Fetch Error: {e}")
            return None
    
    def create_tables(self):
        """Create all required tables for pharmacy management system"""
        
        # TABLE 1: VENDORS/SUPPLIERS
        vendors_table = """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT NOT NULL UNIQUE,
            contact_person TEXT,
            email TEXT,
            phone TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            pin_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # TABLE 2: PRODUCTS/ITEMS
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL UNIQUE,
            product_code TEXT UNIQUE,
            category TEXT,
            unit TEXT,  -- Pieces, Boxes, Bottles, etc.
            purchase_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            current_stock INTEGER DEFAULT 0,
            minimum_stock INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # TABLE 3: PURCHASES
        purchases_table = """
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,
            purchase_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
        )
        """
        
        # TABLE 4: PURCHASE ITEMS (Line items for each purchase)
        purchase_items_table = """
        CREATE TABLE IF NOT EXISTS purchase_items (
            purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
        
        # TABLE 5: PURCHASE RETURNS
        purchase_returns_table = """
        CREATE TABLE IF NOT EXISTS purchase_returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            return_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id)
        )
        """
        
        # TABLE 6: PURCHASE RETURN ITEMS
        purchase_return_items_table = """
        CREATE TABLE IF NOT EXISTS purchase_return_items (
            return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (return_id) REFERENCES purchase_returns(return_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
        
        # TABLE 7: SALES
        sales_table = """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            sale_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT,  -- Cash, Card, UPI, etc.
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # TABLE 8: SALE ITEMS (Line items for each sale)
        sale_items_table = """
        CREATE TABLE IF NOT EXISTS sale_items (
            sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
        
        # TABLE 9: SALES RETURNS
        sales_returns_table = """
        CREATE TABLE IF NOT EXISTS sales_returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            return_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sale_id) REFERENCES sales(sale_id)
        )
        """
        
        # TABLE 10: SALES RETURN ITEMS
        sales_return_items_table = """
        CREATE TABLE IF NOT EXISTS sales_return_items (
            return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (return_id) REFERENCES sales_returns(return_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
        
        # TABLE 11: EXPENSES
        expenses_table = """
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date DATE NOT NULL,
            category TEXT NOT NULL,  -- Rent, Utilities, Salary, etc.
            description TEXT,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # TABLE 12: STOCK TRANSACTIONS (For audit trail)
        stock_transactions_table = """
        CREATE TABLE IF NOT EXISTS stock_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,  -- Purchase, Sale, Return, Adjustment
            quantity_change INTEGER NOT NULL,
            previous_stock INTEGER,
            new_stock INTEGER,
            reference_id INTEGER,  -- Links to purchase_id, sale_id, etc.
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
        
        # Execute all table creation queries
        tables = [
            vendors_table,
            products_table,
            purchases_table,
            purchase_items_table,
            purchase_returns_table,
            purchase_return_items_table,
            sales_table,
            sale_items_table,
            sales_returns_table,
            sales_return_items_table,
            expenses_table,
            stock_transactions_table
        ]
        
        try:
            for table in tables:
                self.execute_query(table)
            print("✓ All tables created successfully!")
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False


# Initialize database when module is imported
def init_database():
    """Initialize database and create tables"""
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_tables()
    db_manager.disconnect()


# Run initialization if this file is executed directly
if __name__ == "__main__":
    init_database()
