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

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(FileManager, self)
        superclass.__init__(path=path, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        return {}

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

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            with file(self._path, 'w') as file_pointer:
                file_pointer.write('')
        self._io_manager.proceed(prompt=prompt)

    def _read_lines(self):
        result = []
        if self._path:
            if os.path.exists(self._path):
                with file(self._path) as file_pointer:
                    result.extend(file_pointer.readlines())
        return result
    
    def _write(self, contents):
        with file(self._path, 'w') as file_pointer:
            file_pointer.write(contents)

    def _write_stub(self):
        self._write(self._unicode_directive)