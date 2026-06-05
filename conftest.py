

import pytest
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, BROWSER, SLOW_MO, SCREENSHOTS_DIR
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@pytest.fixture(scope="function")
def browser():
    """
    Create a browser instance for each test
    scope="function" means new browser for every test
    """
    with sync_playwright() as p:
        # Select browser type
        if BROWSER == "chromium":
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER == "firefox":
            browser = p.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER == "webkit":
            browser = p.webkit.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        else:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """
    Create a new page/tab for each test
    Includes automatic screenshot on failure
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="reports/videos"  # Optional: record video
    )
    page = context.new_page()
    
    yield page
    
    # Take screenshot if test failed
    if hasattr(page, "_test_failed") and page._test_failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOTS_DIR / f"failure_{timestamp}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"\n📸 Screenshot saved: {screenshot_path}")
    
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to detect test failure"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        # Mark that test failed for screenshot fixture
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            item.funcargs["page"]._test_failed = True
