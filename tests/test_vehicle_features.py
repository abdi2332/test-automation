import pytest
from pages.registration_page import RegistrationPage
from pages.gps_page import GPSPage
from config.settings import REGISTRATION_URL, GPS_DASHBOARD_URL, TEST_VEHICLE_ID
import logging

logger = logging.getLogger(__name__)

class TestVehicleFeatures:
    """Test suite for vehicle registration and GPS tracking"""
    
    @pytest.mark.smoke
    def test_vehicle_registration(self, page):
        """
        TC-006: Verify new vehicle registration
        """
        logger.info("=== TC-006: Vehicle Registration ===")
        reg_page = RegistrationPage(page)
        
        vin = "5YJSA1E2XG" # Real Tesla Model S VIN (example)
        owner = "John Doe"
        
        reg_page.navigate(REGISTRATION_URL)
        reg_page.register_vehicle(vin, owner)
        reg_page.verify_registration_success()
        
        # Take evidence
        page.screenshot(path="screenshots/registration_success.png")
        logger.info("✓ TC-006 PASSED")
        
    @pytest.mark.regression
    def test_gps_tracking_dashboard(self, page):
        """
        TC-007: Verify GPS tracking coordinate updates
        """
        logger.info("=== TC-007: GPS Tracking Dashboard ===")
        gps_page = GPSPage(page)
        
        gps_page.navigate(GPS_DASHBOARD_URL)
        
        # Select first vehicle
        gps_page.select_vehicle("TEST-VEHICLE-001")
        gps_page.verify_marker_visible()
        coords_1 = gps_page.get_coordinates()
        assert coords_1["lat"] != "--"
        
        # Select second vehicle
        gps_page.select_vehicle("TEST-VEHICLE-002")
        coords_2 = gps_page.get_coordinates()
        assert coords_2["lat"] != "--"
        
        # Take evidence
        page.screenshot(path="screenshots/gps_dashboard.png")
        logger.info("✓ TC-007 PASSED")
