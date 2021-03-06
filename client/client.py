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
#
# Author: Keyan Pishdadian

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
            self.update_client()
            time.sleep(3)

    def initial_client_sync(self):
        """
        Makes GET requests to download any files on the server.

        Only called when the client is intialized. Checks to see if there are
        any files on the server which are not in the client directory, if yes
        the files are copied to the client directory. This implementation
        assumes that the server's files are the most up to date and so any
        duplicate files are overwritten with the server version of the file.
        """
        files_list = self.poll_server()

        for filename in files_list:
            self.download_from_server(filename)
        return "Client synced to server."

    def update_tracked_file_list(self):
        """
        Updates the client tracked_files dictionary.

        Makes a list of all non-hidden files in the client directory then
        checks to make sure every file is being tracked. If there is no key
        with the same filename present the file and its hash are added to the
        tracked_files dictionary
        """
        current_file_list = self._poll_client()

        # List all files with no previous saved history
        untracked_files = (
            [item for item in current_file_list
             if item not in self.tracked_files.keys()]
        )
        # Add all untracked files to tracked_files dictionary and upload
        for filename in untracked_files:
            file = open(self.abspath+filename, 'rb')
            file_hash = sha1(file.read())
            file.seek(0)
            self.tracked_files[filename] = file_hash
            self.upload_to_server(file)

    def update_server(self):
        """
        Updates hashes in the tracked_files dictionary to reflect any changes.

        Rehashes all the files in the client directory, if the hashes are
        different than those in the tracked_files dictionary then a POST
        request is sent to the server to upload the file. Also responsible
        for keeping track of any deleted files, which are added to the
        delete_list and removed off the server later by update_file_deletes().
        """
        for filename in self.tracked_files.keys():
                try:
                    file = open(self.abspath+filename, 'rb')
                    file_hash = sha1(file.read()).digest()
                    file.seek(0)
                    if not self.tracked_files[filename] == file_hash:
                        self.tracked_files[filename] = file_hash
                        self.upload_to_server(file)
                except IOError:
                    self.delete_list.append(filename)
                    del self.tracked_files[filename]

    def update_file_deletes(self):
        """
        Deletes files from the server to reflect changes in local directory.

        Receives a list of files which are no longer in the client directory
        and iterates through making deletion requests. The delete_list is kept
        up to date by update_server().
        """
        for filename in self.delete_list:
            self.delete_from_server(filename)

        self.delete_list = []

    def update_client(self):
        """
        Ensures that any file changes on the server are made on the client.

        Gets the list of file changes made on the server and either makes
        deletions to client files or downloads server files.
        """
        server_changes = self.get_server_changes()
        for action, filename in server_changes:
            if action == 'delete':
                os.remove(os.path.join(self.abspath, filename))
            elif action == 'add':
                self.download_from_server(filename)

    def poll_server(self):
        """Returns a list of all the files on the server."""
        r = requests.get(self.url + "/file_list")
        try:
            files_list = json.loads(r.content)
        except ValueError:
            return "Server contains no files."

        return files_list

    def get_server_changes(self):
        """Returns a list of changes that were made on the server."""
        client_state = self._poll_client()
        server_state = self.poll_server()
        server_deletions = [('delete', file) for file in client_state
                            if file not in server_state]
        server_additions = [('add', file) for file in server_state
                            if file not in client_state]

        return server_deletions + server_additions

    def upload_to_server(self, file_contents):
        """
        Sends a POST request containing a file to the server.

        The file is sent as a single entry dictionary in the format:
        <key>: the string 'file'
        <value>: the file contents read as bytes
        """

        if file_contents.name in self.system_files:
            return 0
        files = {'file': file_contents}
        r = requests.post(self.url + '/upload/', files=files)
        if r.status_code == 404:
            sys.exit("The server URL you have entered appears to be down.")
        return r

    def delete_from_server(self, filename):
        """
        Sends a GET request which deletes the specified file from the server.
        """
        r = requests.get(self.url+'/delete/'+filename)
        return r

    def download_from_server(self, filename):
        """Downloads the argument file from the server."""
        with open(self.abspath+filename, 'w') as f:
                f.write(requests.get(self.url+'/download/'+filename).content)

    def _poll_client(self):
        """
        Return a list containing all non-hidden files in the current directory.
        """
        files = [file for file in next(os.walk(self.abspath))[2]
                 if not file[0] == '.' and file not in self.system_files]
        return files


if __name__ == "__main__":
    client = flopboxClient(sys.argv[1], os.path.abspath('.'))
    client.loop()
