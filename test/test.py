import unittest
import logging
from app.utils.logging_config import logger  # Adjust the import based on your project structure

class TestLogging(unittest.TestCase):

    def test_logging_output(self):
        with self.assertLogs(logger, level='DEBUG') as log:
            logger.debug('Debug message for testing')
            logger.info('Info message for testing')
            logger.warning('Warning message for testing')
            logger.error('Error message for testing')
            logger.critical('Critical message for testing')

        # Check if the log messages are as expected
        self.assertIn('DEBUG:app.utils.logging_config:Debug message for testing', log.output)
        self.assertIn('INFO:app.utils.logging_config:Info message for testing', log.output)
        self.assertIn('WARNING:app.utils.logging_config:Warning message for testing', log.output)
        self.assertIn('ERROR:app.utils.logging_config:Error message for testing', log.output)
        self.assertIn('CRITICAL:app.utils.logging_config:Critical message for testing', log.output)

if __name__ == '__main__':
    unittest.main()