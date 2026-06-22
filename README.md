# Vehicle Tracking Portal - Test Automation Framework

Professional test automation framework for the Vehicle Tracking Portal, built with Python, Playwright, and Pytest. This framework implements the Page Object Model (POM) architecture to ensure maintainable and scalable end-to-end testing.

## Features

- **Real VIN Decoding**: Integrated with the **NHTSA vPIC API** to automatically fetch vehicle Make, Model, and Year from a real VIN.
- **Persistent Storage**: Utilizes an **SQLite** database (`vehicles.db`) to ensure fleet data persists across server restarts.
- **Live Fleet Tracker**: Real-time mock GPS coordinate simulation and dashboard updates.
- **Page Object Model (POM)**: Decoupled test logic from page-specific actions and locators.
- **Suite Categorization**: Tests are tagged as `smoke`, `regression`, or `slow` for targeted execution.
- **Reporting**: Automated HTML report generation with embedded screenshots and detailed logs.
- **Containerized Execution**: Docker integration for consistent execution across different environments.
- **Failure Analysis**: Screenshots captured automatically at critical test steps and on failures.

## Technology Stack

- **Language**: Python 3.10+
- **Test Runner**: Pytest
- **Web Automation**: Playwright
- **Reporting**: Pytest-HTML
- **Environment**: Docker

## Project Structure

- `tests/`: Contains test suites (e.g., `test_portal.py`).
- `pages/`: Page Object classes defining UI interactions.
- `config/`: Configuration settings and environment variables.
- `data/`: Test data and fixtures.
- `utils/`: Common utility functions.
- `reports/`: Generated test execution reports.
- `screenshots/`: Captured evidence from test runs.

## Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized runs)
- Node.js (for Playwright browser installation)

## Real Portal Setup

The project includes a functional FastAPI-based Vehicle Portal for realistic automation testing.

1. **Install Portal Dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Start the Portal**:
   ```bash
   python -m uvicorn portal_app.main:app --reload
   ```
   The portal will be available at `http://localhost:8000`.

## Running Tests

### Locally

- **Run all features**:
  ```bash
  pytest tests/test_vehicle_features.py
  ```

- **Run core demo tests**:
  ```bash
  pytest tests/test_portal.py
  ```

### Configuration

You can toggle between the demo site and the real portal in `config/settings.py`. Currently, it is configured to target the live FastAPI instance at `http://localhost:8000`.

### Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t test-automation .
   ```

2. **Run tests in container**:
   ```bash
   docker run --rm -v $(pwd)/reports:/app/reports test-automation
   ```

## Reports and Artifacts

After execution, the HTML report can be found in the project root as `report.html` (or in the `reports/` directory if configured). Screenshots taken during the test run are saved in the `screenshots/` directory for audit and debugging purposes.
