import os
from hashlib import sha1
import unittest
import requests

import server
import client


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = "test.txt"
        self.file_contents = open(self.filename, "rb")
        self.url = 'http://127.0.0.1:5000/'

        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        self.client = client.flopboxClient(self.url)

    def tearDown(self):
        pass

    def test_empty_get_request_to_index(self):
        rv = self.app.get('/')
        assert 'index' in rv.data

    def test_simple_post(self):
        # Why is this failing?
        files = {self.filename: self.file_contents}
        r = requests.post(self.url + 'upload/', files=files)
        print r.content
        assert r.status_code == '200'

    def test_upload_file(self):
        # Doesn't do anything yet
        self.client.upload(self.filename, self.file_contents)
        self.fail("Test not finished")

if __name__ == "__main__":
    unittest.main()
