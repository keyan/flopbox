import os
import unittest

import server
import client


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def test_empty_index(self):
        rv = self.app.get('/')
        assert 'index' in rv.data

if __name__ == "__main__":
    unittest.main()
