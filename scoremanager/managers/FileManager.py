# -*- encoding: utf-8 -*-
import os
import traceback
from scoremanager.managers.Manager import Manager


class FileManager(Manager):
    r'''File manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _execute(self, path=None, attribute_names=None):
        assert isinstance(attribute_names, tuple)
        path = path or self._path
        if not os.path.isfile(path):
            return
        with open(path, 'r') as file_pointer:
            file_contents_string = file_pointer.read()
        try:
            exec(file_contents_string)
        except:
            traceback.print_exc()
            self._io_manager.display('')
            return 'corrupt'
        result = []
        for name in attribute_names:
            if name in locals():
                result.append(locals()[name])
            else:
                result.append(None)
        result = tuple(result)
        return result