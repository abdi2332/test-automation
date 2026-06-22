
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Create directories if they don't exist
REPORTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Application URLs
BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/secure"

# Real Portal URLs (FastAPI)
PORTAL_URL = "http://localhost:8000"
REGISTRATION_URL = f"{PORTAL_URL}"
GPS_DASHBOARD_URL = f"{PORTAL_URL}"

# Test credentials (for demo site)
# In real projects, these come from .env file
USERNAME = os.getenv("TEST_USERNAME", "tomsmith")
PASSWORD = os.getenv("TEST_PASSWORD", "SuperSecretPassword!")

# Browser settings
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down execution (ms)

# Timeouts (milliseconds)
DEFAULT_TIMEOUT = 30000
NAVIGATION_TIMEOUT = 60000

# Test data
TEST_VEHICLE_ID = "TEST-VEHICLE-001"
TEST_BUILD_REQUEST = {
    "vehicle_id": TEST_VEHICLE_ID,
    "factory_line": "Bremen-Line-A",
    "priority": "HIGH",
    "status": "PENDING"
}

def get_config_summary():
    """Print current configuration for debugging"""
    return {
        "BASE_URL": BASE_URL,
        "HEADLESS": HEADLESS,
        "BROWSER": BROWSER,
        "REPORTS_DIR": str(REPORTS_DIR)
    }
