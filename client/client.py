#!/usr/bin/env python

# flopbox Client
#
# Run this in the directory to be tracked,
# enter the URL of the server when prompted:
# python client.py
#
# Issues:
# - Design logic doesn't support saving directories recursively
#
# TODO:
# - Registering file deletions
# - Downloading files from the server when run in a new directory
# - Uploading files from the client directory to the server
#
# Author(s): Keyan Pishdadian (and maybe Noah Ennis)

import sys
import os
import time
import json
from hashlib import sha1
import requests


class flopboxClient(object):

    def __init__(self, url, abspath):
        self.system_files = ['client.py',
                             'client.pyc',
                             '__init__.py',
                             '__init__.pyc']
        self.abspath = abspath + '/'
        self.url = url
        if url[-1] == '/':
            self.url = url[0:-1]
        self.tracked_files = {}
        self.delete_list = []
        self.initial_client_sync()

    def loop(self):
        """Infinite loop!"""
        while True:
            self.update_tracked_file_list()
            self.update_server()
            self.update_file_deletes()

    def initial_client_sync(self):
        """
        Makes GET requests to download any files on the server.

        Only called when the client is intialized. Checks to see if there are
        any files on the server which are not in the client directory, if yes
        the files are copied to the client directory. This implementation
        assumes that the server's files are the most up to date and so any
        duplicate files are overwritten with the server version of the file.
        """
        r = requests.get(self.url + "/file_list")
        try:
            files_list = json.loads(r.content)
        except ValueError:
            return "Server contains no files."

        for filename in files_list:
            with open(self.abspath+filename, 'w') as f:
                f.write(requests.get(self.url+'/sync/'+filename).content)
        return "Client synced to server."

    def update_tracked_file_list(self):
        """
        Updates the client tracked_files dictionary.

        Makes a list of all non-hidden files in the client directory then
        checks to make sure every file is being tracked. If there is no key
        with the same filename present the file and its hash are added to the
        tracked_files dictionary
        """
        # List all non-hidden files in current directory
        current_file_list = self._list_files()

        # List all files with no previous saved history
        untracked_files = (
            [item for item in current_file_list
             if item not in self.tracked_files.keys()]
        )
        # Add all untracked files to tracked_files dictionary
        for filename in untracked_files:
            file = open(self.abspath+filename, 'rb')
            file_hash = sha1(file.read())
            file.seek(0)
            self.tracked_files[filename] = file_hash

            # Upload the untracked file
            self.upload_to_server(file)

    def update_file_deletes(self):
        """
        Check if any files were deleted from the client folder and deletes
        them from the server (if they are on the server).
        """
        for filename in self.delete_list:
            self.delete_from_server(filename)

        self.delete_list = []

    def update_server(self):
        """
        Updates hashes in the tracked_files dictionary to reflect any changes.

        Rehashes all the files in the client directory, if the hashes are
        different than those in the tracked_files dictionary then a POST
        request is sent to the server to upload the file.
        """
        for filename in self.tracked_files.keys():
                try:
                    file = open(self.abspath+filename, 'rb')
                    file_hash = sha1(file.read())
                    file.seek(0)
                    if not self.tracked_files[filename] == file_hash:
                        self.tracked_files[filename] = file_hash
                        self.upload_to_server(file)
                except IOError:
                    self.delete_list.append(filename)
                    del self.tracked_files[filename]

    def upload_to_server(self, file_contents):
        """
        Sends a POST request containing a file to the server.

        The file is sent as a single entry dictionary in the format:
        <key>: the filename as a string
        <value>: the sha1 hash of the file contents read as bytes
        """

        if file_contents.name in self.system_files:
            return 0
        files = {'file': file_contents}
        r = requests.post(self.url + '/upload/', files=files)
        if r.status_code == 404:
            print "The server URL you have entered appears to be down."
            self.url = raw_input("Enter the server URL: ")
        return r

    def delete_from_server(self, filename):
        """
        Sends a GET request which deletes the specified file from the server.
        """
        r = requests.get(self.url+'/delete/'+filename)
        return r

    def _list_files(self):
        """
        Return a list containing all non-hidden files in the current directory.

        Ignores directories.
        """
        files = [file for file in next(os.walk(self.abspath))[2]
                 if not file[0] == '.' and file not in self.system_files]
        return files


if __name__ == "__main__":
    client = flopboxClient(sys.argv[1], os.path.abspath('.'))
    client.loop()
