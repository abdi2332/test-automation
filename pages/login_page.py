
from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)

class LoginPage:
    """Page object for the login page"""
    
    # CSS Selectors (locators)
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".flash.success"
    ERROR_MESSAGE = ".flash.error"
    LOGOUT_BUTTON = "text=Logout"
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self):
        """Go to login page"""
        logger.info("Navigating to login page")
        self.page.goto("https://the-internet.herokuapp.com/login")
        return self
    
    def enter_username(self, username: str):
        """Type username into field"""
        logger.info(f"Entering username: {username}")
        self.page.fill(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """Type password into field"""
        logger.info("Entering password")
        self.page.fill(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click the login button"""
        logger.info("Clicking login button")
        self.page.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """Complete login flow"""
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_success_message(self) -> str:
        """Get success message text"""
        expect(self.page.locator(self.SUCCESS_MESSAGE)).to_be_visible()
        return self.page.locator(self.SUCCESS_MESSAGE).text_content()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_visible()
        return self.page.locator(self.ERROR_MESSAGE).text_content()
    
    def is_logged_in(self) -> bool:
        """Check if user successfully logged in"""
        return "secure" in self.page.url
    
    def logout(self):
        """Log out from the application"""
        logger.info("Logging out")
        self.page.click(self.LOGOUT_BUTTON)
        return self
