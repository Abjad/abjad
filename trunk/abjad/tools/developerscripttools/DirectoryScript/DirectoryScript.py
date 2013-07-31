# -*- encoding: utf-8 -*-
import argparse
import os
from abjad.tools.developerscripttools.DeveloperScript import DeveloperScript


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
        message = '{!r} is not a valid directory.'
        error = argparse.ArgumentTypeError(message.format(path))
        path = os.path.abspath(path)
        if not self._is_valid_path(path):
            raise error
        return os.path.relpath(path)
