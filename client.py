# flopbox Client
#
# Run this in the directory to be tracked:
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
from hashlib import sha1
import requests


class flopboxClient(object):

    def __init__(self):
        self.url = raw_input("Enter the server URL: ")
        self.tracked_files = {}
        self.download()  # This doesn't do anything yet.
        self.loop()  # Infinite loop!

    def loop(self):
        while True:
            self.update_tracked_file_list()
            self.update_server()
            time.sleep(3)

    def update_tracked_file_list(self):
        """
        Updates the client tracked_files dictionary.

        Makes a list of all non-hidden files in the client directory then
        checks to make sure every file is being tracked. If there is no key
        with the same filename present the file and its hash are added to the
        tracked_files dictionary
        """
        # List all non-hidden files in current directory
        file_list = self._list_files()

        # List all files with no previous saved history
        untracked_files = (
            [item for item in file_list
             if item not in self.tracked_files.keys()]
        )
        # Add all untracked files to tracked_files dictionary
        for filename in untracked_files:
            file_contents = open(filename, 'rb')
            file_hash = sha1(file_contents).read()
            file_contents.seek(0)
            self.tracked_files[filename] = file_hash

            # Upload the untracked file
            self.upload(filename, file_contents)

    def update_server(self):
        """
        Updates hashes in the tracked_files dictionary to reflect any changes.

        Rehashes all the files in the client directory, if the hashes are
        different than those in the tracked_files dictionary then a POST
        request is sent to the server to upload the file.
        """
        for filename in self.tracked_files.keys():
                file_contents = open(filename, 'rb')
                file_hash = sha1(file_contents.read())
                file_contents.seek(0)
                if not self.tracked_files[filename] == file_hash:
                    self.tracked_files[filename] = file_hash
                    self.upload(filename, file_contents)

    def upload(self, filename, file_contents):
        """
        Sends a POST request containing a file to the server.

        The file is sent as a single entry dictionary in the format:
        <key>: the filename as a string
        <value>: the sha1 hash of the file contents read as bytes
        """
        files = {filename: file_contents}
        r = requests.post(self.url + '/upload/', files=files)
        if r.status_code == 404:
            print "The server URL you have entered appears to be down."
            self.url = raw_input("Enter the server URL: ")

    def download(self):
        """
        Makes GET requests to download any files on the server.

        Only called when the client is intialized, after which file removal is
        handled through delete() calls.
        """
        pass
        # r = requests.get(self.url + "/file_list")
        # TODO: All the things

    def delete(self):
        """
        Check if any files are not present in the client folder and delete
        them from the server (if they are on the server).
        """
        pass
        # TODO: All the things

    def _list_files(self):
        """
        Return a list containing all non-hidden files in the current directory.
        """
        files = [file for file in next(os.walk('.'))[2] if not file[0] == '.']

        return files


if __name__ == "__main__":
    flopboxClient()
