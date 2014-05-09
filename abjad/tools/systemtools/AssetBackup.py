# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad.tools.abctools.ContextManager import ContextManager


class AssetBackup(ContextManager):
    r'''Asset backup context manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_backup_paths',
        '_paths',
        '_remove',
        )

    ### INITIALIZER ###

    def __init__(self, paths=None, remove=None):
        paths = paths or []
        assert isinstance(paths, (list, tuple)), repr(paths)
        paths = tuple(paths)
        self._paths = paths
        remove = remove or []
        assert isinstance(remove, (list, tuple)), repr(remove)
        self._remove = remove

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Backs up assets.

        Returns none.
        '''
        for path in self.remove:
            assert not os.path.exists(path)
        assert all(os.path.exists(_) for _ in self.paths)
        assert all(os.path.isfile(_) or os.path.isdir(_) for _ in self.paths)
        backup_paths = []
        for path in self.paths:
            backup_path = path + '.backup'
            if os.path.isfile(path):
                shutil.copyfile(path, backup_path)
                assert filecmp.cmp(path, backup_path)
            elif os.path.isdir(path):
                shutil.copytree(path, backup_path)
            else:
                message = 'neither file nor directory: {}.'
                message = message.format(path)
                raise TypeError(message)
            backup_paths.append(backup_path)
        backup_paths = tuple(backup_paths)
        self._backup_paths = backup_paths

    def __exit__(self, exg_type, exc_value, trackeback):
        r'''Restores assets and removes backups;
        also removes paths in remove list.

        Returns none.
        '''
        assert all(os.path.exists(_) for _ in self.paths)
        assert all(os.path.exists(_) for _ in self.backup_paths)
        assert len(self.paths) == len(self.backup_paths)
        for path in self.paths:
            backup_path = path + '.backup'
            if os.path.isfile(path):
                os.remove(backup_path)
                shutil.copyfile(backup_path, path)
                filecmp.cmp(path, backup_path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
                shutil.copytree(backup_path, path)
                shutil.rmtree(backup_path)
        assert all(os.path.exists(_) for _ in self.paths)
        assert not any(os.path.exists(_) for _ in self.backup_paths)
        for path in self.remove:
            if os.path.exists:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    pass

    ### PUBLIC PROPERTIES ###

    @property
    def backup_paths(self):
        r'''Gets asset backup paths.

        Returns tuple.
        '''
        return self._backup_paths

    @property
    def paths(self):
        r'''Gets asset paths.

        Returns tuple.
        '''
        return self._paths

    @property
    def remove(self):
        r'''Gets paths to remove on exit.

        Returns tuple.
        '''
        return self._remove