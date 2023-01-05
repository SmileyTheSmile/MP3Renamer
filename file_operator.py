from os import listdir, rename
from pathlib import Path
from os.path import isfile, splitext, join


class FileOperator:
    def get_files_from_directory(self, directory, supported_extensions=None, check_if_valid=True):
        """Get a list of file names in a given directory"""
        directory = Path(directory).resolve()
        files = listdir(directory)

        if check_if_valid:
            files = self.check_for_valid_files(files, directory)
        if supported_extensions is not None:
            files = self.check_for_supported_files(files, supported_extensions)

        return files

    def check_for_valid_files(self, files, song_directory):
        """Check if the strings in a list are files in a given directory."""
        return [file for file in files if isfile(join(song_directory, file))]

    def check_for_supported_files(self, files, supported_extensions):
        """Check if the extensions of the files in a list are supported."""
        return [file for file in files if splitext(file)[1] in supported_extensions]
