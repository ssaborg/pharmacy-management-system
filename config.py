# config.py - Configuration file for Pharmacy Management System
# PLACEMENT: Root directory of project (pharmacy-management-system/config.py)

import os

# Database configuration
DATABASE_NAME = "pharmacy.db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

# Application settings
APP_TITLE = "Pharmacy Management System"
APP_VERSION = "1.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# UI Colors
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
DANGER_COLOR = "#e74c3c"
WARNING_COLOR = "#f39c12"
LIGHT_COLOR = "#ecf0f1"

# Date format
DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
