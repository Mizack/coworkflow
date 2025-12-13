@echo off
echo ========================================
echo CoworkFlow - Test Runner
echo ========================================

set PYTHONPATH=%cd%

if "%1"=="unit" (
    echo Running Unit Tests...
    pytest tests/unit/ -v --tb=short --cov=. --cov-report=html
    goto :end
)

if "%1"=="integration" (
    echo Running Integration Tests...
    echo Starting Docker containers...
    docker-compose up -d
    timeout /t 30 /nobreak
    pytest tests/integration/ -v --tb=short
    docker-compose down
    goto :end
)

if "%1"=="ui" (
    echo Running UI Tests...
    echo Starting services...
    docker-compose up -d
    timeout /t 30 /nobreak
    pytest tests/ui/ -v --tb=short
    docker-compose down
    goto :end
)

if "%1"=="e2e" (
    echo Running E2E Tests...
    echo Starting all services...
    docker-compose up -d
    timeout /t 45 /nobreak
    pytest tests/e2e/ -v --tb=short
    docker-compose down
    goto :end
)

if "%1"=="performance" (
    echo Running Performance Tests...
    echo Starting services...
    docker-compose up -d
    timeout /t 30 /nobreak
    locust -f tests/performance/load_test.py --host=http://localhost:8000 --users=10 --spawn-rate=2 --run-time=60s --headless
    docker-compose down
    goto :end
)

if "%1"=="all" (
    echo Running All Tests...
    call %0 unit
    call %0 integration
    call %0 ui
    call %0 e2e
    goto :end
)

echo Usage: run-tests.bat [unit|integration|ui|e2e|performance|all]
echo.
echo   unit        - Run unit tests only
echo   integration - Run integration tests
echo   ui          - Run UI tests with Selenium
echo   e2e         - Run end-to-end tests
echo   performance - Run performance/load tests
echo   all         - Run all test suites

:end
echo Tests completed!