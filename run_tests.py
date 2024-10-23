import unittest

# Import all test modules
from tests.test_api import TestOpenWeatherMapAPI
from tests.test_data_processing import TestWeatherAggregator
from tests.test_alerting import TestAlertSystem
from tests.test_visualization import TestDataVisualizer

# Create a test suite
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestOpenWeatherMapAPI))
    test_suite.addTest(unittest.makeSuite(TestWeatherAggregator))
    test_suite.addTest(unittest.makeSuite(TestAlertSystem))
    test_suite.addTest(unittest.makeSuite(TestDataVisualizer))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
