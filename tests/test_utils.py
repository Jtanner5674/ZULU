import unittest
from utils import current_time, open_browser

class TestUtilsModule(unittest.TestCase):

    def test_current_time(self):
        # Test if current_time function returns a correctly formatted string
        time = current_time()
        self.assertIn("The current time is", time)

    def test_open_browser(self):
        # Test open_browser with a known input
        result = open_browser("open google.com")
        self.assertEqual(result, "Opening: google.com")


if __name__ == '__main__':
    unittest.main()
