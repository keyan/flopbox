import os
from hashlib import sha1
import unittest
import shutil

import requests

from server import server
from client import client


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.client_path = os.path.join(os.path.abspath('.'), 'client')
        self.server_path = os.path.join(os.path.abspath('.'), 'server')
        self.uploads_path = os.path.join(self.server_path, 'uploads')
        self.url = 'http://127.0.0.1:5000/'
        self.client = client.flopboxClient(self.url, self.client_path)

        self.filename = "test.txt"
        with open('./client/'+self.filename, 'w') as f:
            f.write('test')
        with open('./client/test2.txt', 'w') as f:
            f.write('test')

    def tearDown(self):
        """Clean up by removing all backed up files."""
        shutil.rmtree(self.uploads_path)
        os.mkdir(self.uploads_path)
        os.remove(self.client_path+'/test.txt')
        os.remove(self.client_path+'/test2.txt')

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
        with open('./client/'+self.filename, "rb") as f:
            file = f
            files = {'file': file}
            r = requests.post(self.url+'upload/', files=files)
        assert r.status_code == 200
        assert self.filename in os.listdir(self.uploads_path)

    def test_upload_with_client(self):
        """Tests whether the client can upload a file to the server."""
        with open(self.client_path+'/'+self.filename, "rb") as f:
            file = f
            r = self.client.upload_to_server(file)
        assert r.status_code == 200
        assert self.filename in os.listdir(self.uploads_path)

    def test_simple_sync_file(self):
        assert self.filename not in os.listdir(self.uploads_path)
        self.client.update_tracked_file_list()
        self.client.update_server()
        assert self.filename in os.listdir(self.uploads_path)

    def test_sync_file_after_changes(self):
        """Tests if changing an existing file results in re-uploading."""
        with open(self.client_path+'/'+self.filename, 'w') as f:
            f.write('testing 1 2 3')

        self.client.update_tracked_file_list()
        self.client.update_server()

        with open(self.uploads_path+'/'+self.filename, 'rb') as f:
            contents = f.readline()
        assert contents == 'testing 1 2 3'

    def test_creating_new_file_results_in_upload(self):
        """
        Tests if a new file addition is recognized by the client and
        handled with an upload.
        """
        with open(self.client_path+'/test2.txt', 'w') as f:
            f.write('testing')
        self.client.update_tracked_file_list()
        self.client.update_server()
        assert 'test2.txt' in os.listdir(self.uploads_path)

    def test_delete_file_on_client_results_in_delete_on_server(self):
        assert self.filename in os.listdir(self.uploads_path)
        assert self.filename in os.listdir(self.client_path)
        os.remove(self.client_path+'/'+self.filename)
        assert self.filename not in os.listdir(self.client_path)

        self.update_file_deletes()
        assert self.filename not in os.listdir(self.uploads_path)

if __name__ == "__main__":
    unittest.main()
    # TODO: Path problems with the file listing function
