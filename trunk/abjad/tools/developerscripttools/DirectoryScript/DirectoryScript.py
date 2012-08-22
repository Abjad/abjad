from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript
import argparse
import os


class DirectoryScript(DeveloperScript):
    '''`DirectoryScript` provides utilities for validating file system paths.

    `DirectoryScript` is abstract.
    '''

    ### PRIVATE METHODS ###

    def _is_valid_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    def _validate_path(self, path):
        error = argparse.ArgumentTypeError('{!r} is not a valid directory.'.format(path))
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return os.path.relpath(path)
