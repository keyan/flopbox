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

        self.client = client.flopboxClient(self.url)

    def tearDown(self):
        pass

    def test_empty_get_to_index(self):
        r = requests.get(self.url)
        assert 'GET' in r.content

    def test_empty_post_to_index(self):
        r = requests.post(self.url)
        assert 'POST' in r.content

    def test_upload_with_manual_post_request(self):
        file = {'file': self.file_contents}
        r = requests.post(self.url+'upload/', files=file)
        print r.content
        assert r.status_code == 200

    def test_upload_with_client(self):
        # Doesn't do anything yet
        self.client.upload(self.filename, self.file_contents)
        # self.fail("Test not finished")

if __name__ == "__main__":
    unittest.main()
