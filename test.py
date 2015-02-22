import os
from hashlib import sha1
import unittest
import shutil

import requests

import server
import client


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = "test.txt"
        self.file = open(self.filename, "rb")
        self.url = 'http://127.0.0.1:5000/'

        self.client = client.flopboxClient(self.url)

    def tearDown(self):
        """Clean up by removing all backed up files."""
        shutil.rmtree('./uploads/')
        os.mkdir('./uploads')

    def test_empty_get_to_index(self):
        """
        Index page just returns 'GET' for now.

        This test will have to change if a web interface is added.
        """
        r = requests.get(self.url)
        assert 'GET' in r.content

    def test_empty_post_to_index(self):
        """
        Index page just returns 'POST' for now.

        This test will have to change if a web interface is added.
        """
        r = requests.post(self.url)
        assert 'POST' in r.content

    def test_upload_with_manual_post_request(self):
        """Tests whether a file can be manually uploaded to the server."""
        files = {'file': self.file}
        r = requests.post(self.url+'upload/', files=files)
        assert r.status_code == 200
        assert self.filename in os.listdir('./uploads')
        os.remove('./uploads/' + self.filename)

    def test_upload_with_client(self):
        """Tests whether the client can upload a file to the server."""
        r = self.client.upload(self.file)
        assert r.status_code == 200
        assert self.filename in os.listdir('./uploads')

    def test_sync_files_in_current_directory(self):
        """Tests whether starting the client loop results in file sync."""
        self.client.update_tracked_file_list()
        self.client.update_server()
        assert 'client.py' in os.listdir('./uploads')

    def test_sync_file_after_changes(self):
        """Tests if changing an existing file results in re-uploading."""
        pass

    def test_create_new_file_results_in_upload(self):
        """
        Tests if a new file addition is recognized by the client and
        handled with an upload.
        """
        open('test2.txt', 'w')
        self.client.update_tracked_file_list()
        self.client.update_server()
        assert 'test2.txt' in os.listdir('./uploads')
        os.remove('test2.txt')

if __name__ == "__main__":
    unittest.main()
