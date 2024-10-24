import unittest
import sys
from main import main as create_post
sys.path.insert(0, '..')


class TestTheBot(unittest.TestCase):
    def test_1_bot_result(self):
        result = create_post()
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
