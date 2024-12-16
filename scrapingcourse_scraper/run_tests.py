import os
import unittest
import coverage
import sys

def run_tests():
    # Get the absolute path to the tests directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    start_dir = os.path.join(current_dir, 'tests')
    
    # Create a coverage instance
    cov = coverage.Coverage(config_file='.coveragerc')
    
    # Start coverage
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir)
    
    # Create a runner with minimal output (only test run summary)
    runner = unittest.TextTestRunner(verbosity=1)  # Reduced verbosity to show pass/fail summary
    result = runner.run(suite)
    
    # Stop coverage
    cov.stop()
    
    # Generate coverage report
    cov.report()  # This will show the overall coverage
    cov.html_report(directory='htmlcov')  # Generate an HTML report for detailed view
    
    # Only print the test coverage summary and ignore the test errors
    if result.wasSuccessful():
        print("All tests passed.")
    else:
        print("Some tests failed.")
    
    # Return test success result (True if passed, False if failed)
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    # Exit with status 0 if successful, 1 if failed
    sys.exit(0 if success else 1)
