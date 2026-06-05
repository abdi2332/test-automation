

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.settings import USERNAME, PASSWORD, TEST_BUILD_REQUEST
import logging

logger = logging.getLogger(__name__)


class TestVehiclePortal:
    """Test class for vehicle tracking portal functionality"""
    
    @pytest.mark.smoke
    def test_successful_login(self, page):
        """
        TC-001: Verify user can login with valid credentials
        Industrial: QA validates operator authentication
        """
        logger.info("=== TC-001: Successful Login ===")
        
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Perform login
        login_page.login(USERNAME, PASSWORD)
        
        # Verify successful login
        dashboard_page.verify_successful_login()
        
        # Take screenshot as evidence
        dashboard_page.take_screenshot("after_login")
        
        logger.info("✓ TC-001 PASSED")
    
    @pytest.mark.smoke
    def test_failed_login_wrong_password(self, page):
        """
        TC-002: Verify login fails with incorrect password
        Industrial: Security validation
        """
        logger.info("=== TC-002: Failed Login ===")
        
        login_page = LoginPage(page)
        
        login_page.navigate()
        login_page.enter_username(USERNAME)
        login_page.enter_password("wrongpassword")
        login_page.click_login_button()
        
        # Verify error message
        error_text = login_page.get_error_message()
        assert "Your password is invalid" in error_text
        
        # Verify still on login page
        assert not login_page.is_logged_in()
        
        logger.info("✓ TC-002 PASSED")
    
    @pytest.mark.regression
    def test_logout_functionality(self, page):
        """
        TC-003: Verify user can logout successfully
        """
        logger.info("=== TC-003: Logout Functionality ===")
        
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Login first
        login_page.login(USERNAME, PASSWORD)
        dashboard_page.verify_successful_login()
        
        # Logout
        dashboard_page.logout()
        
        # Verify back on login page
        assert "login" in page.url
        logger.info("✓ TC-003 PASSED")
    
    @pytest.mark.regression
    def test_multiple_login_logout_cycles(self, page):
        """
        TC-004: Test multiple login/logout cycles
        Industrial: Session handling validation
        """
        logger.info("=== TC-004: Multiple Login/Logout Cycles ===")
        
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        for cycle in range(1, 4):
            logger.info(f"Cycle {cycle}/3")
            login_page.login(USERNAME, PASSWORD)
            dashboard_page.verify_successful_login()
            dashboard_page.logout()
        
        logger.info("✓ TC-004 PASSED")
    
    @pytest.mark.slow
    def test_build_request_submission_simulation(self, page):
        """
        TC-005: Simulate build request submission
        Industrial: Production order processing
        """
        logger.info("=== TC-005: Build Request Submission ===")
        
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Login
        login_page.login(USERNAME, PASSWORD)
        dashboard_page.verify_successful_login()
        
        # Simulate build request submission
        # In a real test, you would:
        # 1. Click "New Build Request" button
        # 2. Fill form with TEST_BUILD_REQUEST data
        # 3. Click Submit
        # 4. Verify success message
        
        logger.info(f"Simulated submission for: {TEST_BUILD_REQUEST['vehicle_id']}")
        dashboard_page.take_screenshot("after_submission")
        
        logger.info("✓ TC-005 PASSED")
