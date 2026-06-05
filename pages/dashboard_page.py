from playwright.sync_api import Page, expect
import logging
from datetime import datetime
from config.settings import SCREENSHOTS_DIR

logger = logging.getLogger(__name__)

class DashboardPage:
    """Page object for the secure dashboard"""
    
    SUCCESS_BANNER = ".flash.success"
    CONTENT_AREA = "#content"
    LOGOUT_BUTTON = "text=Logout"
    
    def __init__(self, page: Page):
        self.page = page
    
    def verify_successful_login(self):
        """Assert user is on dashboard"""
        logger.info("Verifying successful login")
        expect(self.page).to_have_url("https://the-internet.herokuapp.com/secure")
        expect(self.page.locator(self.SUCCESS_BANNER)).to_contain_text(
            "You logged into a secure area"
        )
        return self
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.page.title()
    
    def take_screenshot(self, name: str = None):
        """Save screenshot for reporting"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = name or f"screenshot_{timestamp}"
        path = SCREENSHOTS_DIR / f"{filename}.png"
        self.page.screenshot(path=str(path))
        logger.info(f"Screenshot saved: {path}")
        return str(path)
    
    def get_welcome_message(self) -> str:
        """Extract welcome text from dashboard"""
        content = self.page.locator(self.CONTENT_AREA).text_content()
        return content
    
    def logout(self):
        """Logout from dashboard"""
        logger.info("Logging out from dashboard")
        with self.page.expect_navigation():
            self.page.click(self.LOGOUT_BUTTON)
        logger.info("Logout navigation complete")
        return self