

from playwright.sync_api import sync_playwright
import pytest
from datetime import datetime

# This runs before each test - sets up the browser
@pytest.fixture
def browser():
    """Launch a browser and close it after the test"""
    with sync_playwright() as p:
        # headless=True means no browser window appears (runs in background)
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

# TEST 1: Successful login
def test_successful_login(browser):
    """User can log in with valid credentials"""
    
    # Create a new page/tab
    page = browser.new_page()
    
    # Go to the login page
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Fill in username and password
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    
    # Click the login button
    page.click("button[type='submit']")
    
    # Check if success message appears
    success_message = page.locator(".flash.success")
    assert success_message.is_visible(), "Login failed - success message not found"
    
    print("✓ Test passed: Successfully logged in")

# TEST 2: Failed login with wrong password
def test_failed_login_with_wrong_password(browser):
    """Wrong password shows error message"""
    
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Enter wrong password
    page.fill("#username", "tomsmith")
    page.fill("#password", "wrongpassword")
    page.click("button[type='submit']")
    
    # Check if error message appears
    error_message = page.locator(".flash.error")
    assert error_message.is_visible(), "Error message not shown for wrong password"
    
    print("✓ Test passed: Wrong password correctly rejected")

# TEST 3: Take screenshot (for debugging/reports)
def test_take_screenshot_on_dashboard(browser):
    """Take a screenshot after login"""
    
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")
    
    # Take screenshot with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshot_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    
    # Verify we're on the secure page
    assert "secure" in page.url, "Not on secure page after login"
    
    print(f"✓ Test passed: Screenshot saved to {screenshot_path}")
