import unittest
import functions

class LogTest(unittest.TestCase):
    # test writes correctly to file

    # test assertion catches invalid filepath
    def test_invalid_path_assertion(self):
        self.assertRaises(AssertionError, functions.log, 'this is a test message', '/this/is/an/invalid/path')

    # test messages are appended
