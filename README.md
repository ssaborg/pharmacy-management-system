# Pharmacy Management System

A comprehensive desktop application for managing pharmacy/medical store operations using Python (Tkinter) and SQLite3.

## Features

✅ **Vendor/Supplier Management** - Add, edit, delete vendors  
✅ **Product/Item Management** - Manage inventory items with pricing  
✅ **Purchase Management** - Record purchases from vendors  
✅ **Purchase Return** - Handle purchase returns  
✅ **Sales Management** - Record customer sales  
✅ **Sales Return** - Process sales returns  
✅ **Stock Management** - Real-time inventory tracking  
✅ **Expense Management** - Track business expenses  
✅ **Profit & Loss Report** - Comprehensive P&L analysis  
✅ **Analysis Reports** - Detailed business analytics  

## Project Structure

```
pharmacy-management-system/
├── main.py                 # Entry point of application
├── config.py              # Configuration settings
├── database.py            # Database schema and initialization
├── modules/
│   ├── __init__.py
│   ├── vendor.py          # Vendor management
│   ├── product.py         # Product management
│   ├── purchase.py        # Purchase operations
│   ├── sales.py           # Sales operations
│   ├── stock.py           # Stock management
│   ├── expense.py         # Expense tracking
│   └── reports.py         # Reports and analytics
├── ui/
│   ├── __init__.py
│   ├── windows.py         # Main UI windows
│   └── styles.py          # UI styling
└── pharmacy.db            # SQLite database (auto-created)
```

## Installation

1. Clone this repository
2. Install Python 3.8+
3. Run: `python main.py`

## Requirements

- Python 3.8+
- Tkinter (comes with Python)
- SQLite3 (built-in with Python)

## License

Open Source - Commercial Use Allowed

---
**Created for: Professional Pharmacy Store Management**
