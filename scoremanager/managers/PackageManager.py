# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from scoremanager.managers.DirectoryManager import DirectoryManager


class PackageManager(DirectoryManager):
    r'''Package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_package_name',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert os.path.sep in path
        DirectoryManager.__init__(
            self,
            path=path,
            session=session,
            )
        package_name = None
        if path is not None:
            self._package_name = os.path.basename(self._path)

    ### PRIVATE PROPERTIES ###

    @property
    @systemtools.Memoize
    def _initializer_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )

    @property
    def _initializer_file_path(self):
        return os.path.join(self._path, '__init__.py')

    @property
    def _user_input_to_action(self):
        superclass = super(PackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'ino': self.open_initializer,
            'inws': self.write_initializer_stub,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_next_asset = False
        self._session._is_navigating_to_previous_asset = False
        self._session._last_asset_path = self._path

    def _make_main_menu(self, name='package manager'):
        menu = self._io_manager.make_menu(name=name)
        return menu

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    ### PUBLIC METHODS ###

    def open_initializer(self):
        r'''Opens initializer.

        Returns none.
        '''
        self._initializer_file_manager.view()

    def write_initializer_stub(self, prompt=True):
        r'''Writes initializer stub.

        Returns none.
        '''
        path = self._initializer_file_path
        if prompt:
            message = 'will write stub to {}.'
            message = message.format(path)
            self._io_manager.display(message)
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
        manager = self._io_manager.make_file_manager(path)
        manager._write_stub()
        if prompt:
            message = 'wrote stub to {}.'
            message = message.format(path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True