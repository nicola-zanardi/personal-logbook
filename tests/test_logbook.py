import unittest

import logbook


class LogbookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = logbook.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Personal Logbook', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
