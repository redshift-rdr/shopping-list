import unittest, os
import functions

class LogTest(unittest.TestCase):
    # test writes correctly to file
    def test_file_write(self):
        functions.log("[DEBUG] this is a test", "logtest")

        with open("logtest", 'r') as f:
            data = f.read()

        self.assertRegex(data, r'\[(\d*)-(\d*)-(\d*) (\d*):(\d*):(\d*)\] - (.*)')

    # test messages are appended
    def test_file_append(self):
        functions.log("[DEBUG] this is a test", "logtest")
        functions.log("[DEBUG] this is a second line", "logtest")

        with open("logtest", 'r') as f:
            data = f.read()

        self.assertRegex(data, r'\[(\d*)-(\d*)-(\d*) (\d*):(\d*):(\d*)\] - \[DEBUG\] this is a test\n')
        self.assertRegex(data, r'\[(\d*)-(\d*)-(\d*) (\d*):(\d*):(\d*)\] - \[DEBUG\] this is a second line')

    def tearDown(self) -> None:
        os.remove("logtest")
