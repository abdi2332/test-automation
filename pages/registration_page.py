from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)

class RegistrationPage:
    """Page object for the Vehicle Registration form"""
    
    NAV_LINK = "text=Add Vehicle"
    VIN_INPUT = "#vinInput"
    MODEL_SELECT = "#modelSelect"
    OWNER_INPUT = "#ownerInput"
    SUBMIT_BUTTON = "#submitReg"
    SUCCESS_MESSAGE = "#successMsg"
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Navigate to the portal and open registration section"""
        logger.info(f"Navigating to Portal: {url}")
        self.page.goto(url)
        self.page.click(self.NAV_LINK)
        return self
    
    def register_vehicle(self, vin: str, owner: str):
        """Fill and submit registration form"""
        logger.info(f"Registering vehicle: {vin} for {owner}")
        self.page.fill(self.VIN_INPUT, vin)
        self.page.fill(self.OWNER_INPUT, owner)
        self.page.click(self.SUBMIT_BUTTON)
        return self
    
    def verify_registration_success(self):
        """Assert success message is visible"""
        logger.info("Verifying registration success")
        expect(self.page.locator(self.SUCCESS_MESSAGE)).to_be_visible()
        return self
