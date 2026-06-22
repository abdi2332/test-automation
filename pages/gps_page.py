from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)

class GPSPage:
    """Page object for the GPS Tracking Dashboard"""
    
    NAV_LINK = "text=Fleet View"
    VEHICLE_LIST_ITEMS = ".vehicle-item"
    LAT_DISPLAY = "#lat"
    LNG_DISPLAY = "#lng"
    VEHICLE_POINTER = "#vehicle-marker"
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Navigate to the portal and open fleet section"""
        logger.info(f"Navigating to GPS Dashboard: {url}")
        self.page.goto(url)
        self.page.click(self.NAV_LINK)
        return self
    
    def select_vehicle(self, vehicle_id: str):
        """Click on a vehicle in the fleet list"""
        logger.info(f"Selecting vehicle: {vehicle_id}")
        self.page.click(f"text={vehicle_id}")
        return self
    
    def get_coordinates(self) -> dict:
        """Extract current lat/lng from dashboard"""
        # Wait for value to be updated from "--"
        expect(self.page.locator(self.LAT_DISPLAY)).not_to_contain_text("--")
        lat = self.page.locator(self.LAT_DISPLAY).text_content()
        lng = self.page.locator(self.LNG_DISPLAY).text_content()
        logger.info(f"Current coordinates: {lat}, {lng}")
        return {"lat": lat, "lng": lng}
    
    def verify_marker_visible(self):
        """Ensure vehicle marker is displayed on map"""
        expect(self.page.locator(self.VEHICLE_POINTER)).to_be_visible()
        return self
