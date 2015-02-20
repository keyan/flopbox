import sys
import os
import hashlib


class flopboxClient(object):

    def __init__(self):
        self.server_address = raw_input("Enter the server address: ")
        self.tracked_files = {}
        self.download()

    def loop(self):
        while True:
            # List all non-hidden files in current directory
            file_list = self._list_files()

            # List all files with no previous saved history
            untracked_files = (
                [item for item in file_list
                 if item not in self.tracked_files.keys()]
            )
            # Add all untracked files to tracked dictionary with a new hash
            for each_file in untracked_files:
                file_contents = open(each_file, 'rb').read()
                self.tracked_files[each_file] = hashlib.sha256(file_contents)

                # Upload the untracked file
                self.upload(each_file)

            # Check all tracked files and update any with changed hashes
            for file in self.tracked_files.keys():
                file_contents = open(each_file, 'rb').read()
                file_hash = hashlib.sha256(file_contents)
                if not self.tracked_files[file] == file_hash:
                    self.tracked_files[file] = file_hash
                    self.upload(file)

            # TODO check if any files are not present in the client folder
            # and delete() them from the server (if they are on the server)

    def upload(self):
        pass

    def download(self):
        pass

    def delete(self):
        pass

    def _list_files(self):
        """
        Returns a list containing all the files and directories in the current
        directory which are not hidden (unlike os.listdir())
        """
        filelist = []
        for each_file in os.listdir('.'):
            if not each_file.startswith('.'):
                filelist.append(each_file)

        return filelist


if __name__ == "__main__":
    flopboxClient()
