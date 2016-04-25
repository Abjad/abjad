# -*- coding: utf-8 -*-
import filecmp
import os
import shutil
from abjad.tools.abctools.ContextManager import ContextManager


class FilesystemState(ContextManager):
    r'''Filesystem state context manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_keep',
        '_remove',
        )

    ### INITIALIZER ###

    def __init__(self, keep=None, remove=None):
        keep = keep or []
        assert isinstance(keep, (list, tuple)), repr(keep)
        keep = tuple(keep)
        self._keep = keep
        remove = remove or []
        assert isinstance(remove, (list, tuple)), repr(remove)
        self._remove = remove

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Backs up filesystem assets.

        Returns none.
        '''
        for path in self.remove:
            assert not os.path.exists(path), repr(path)
        for path in self.keep:
            assert os.path.exists(path), repr(path)
            assert os.path.isfile(path) or os.path.isdir(path), repr(path)
        for path in self.keep:
            backup_path = path + '.backup'
            if os.path.isfile(path):
                shutil.copyfile(path, backup_path)
                assert filecmp.cmp(path, backup_path), repr(path)
            elif os.path.isdir(path):
                shutil.copytree(path, backup_path)
            else:
                message = 'neither file nor directory: {}.'
                message = message.format(path)
                raise TypeError(message)

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Restores filesytem assets and removes backups;
        also removes paths in remove list.

        Returns none.
        '''
        backup_paths = (_ + '.backup' for _ in self.keep)
        for path in backup_paths:
            assert os.path.exists(path), repr(path)
        for path in self.keep:
            backup_path = path + '.backup'
            assert os.path.exists(backup_path), repr(backup_path)
            if os.path.isfile(backup_path):
                shutil.copyfile(backup_path, path)
                filecmp.cmp(path, backup_path)
                os.remove(backup_path)
            elif os.path.isdir(backup_path):
                if os.path.exists(path):
                    shutil.rmtree(path)
                shutil.copytree(backup_path, path)
                shutil.rmtree(backup_path)
            else:
                message = 'neither file nor directory: {}.'
                message = message.format(path)
                raise TypeError(message)
        for path in self.remove:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    message = 'neither file nor directory: {}.'
                    message = message.format(path)
                    raise TypeError(message)
        for path in self.keep:
            assert os.path.exists(path), repr(path)
        for path in backup_paths:
            assert not os.path.exists(path), repr(path)

    ### PUBLIC PROPERTIES ###

    @property
    def keep(self):
        r'''Gets asset paths to restore on exit.

        Returns tuple.
        '''
        return self._keep

    @property
    def remove(self):
        r'''Gets paths to remove on exit.

        Returns tuple.
        '''
        return self._remove
