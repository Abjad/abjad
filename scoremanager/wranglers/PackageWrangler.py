# -*- encoding: utf-8 -*-
import os
from scoremanager.wranglers.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.

    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(PackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_package,
            'new': self.make_package,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            #
            'mdls*': self.list_every_metadata_py,
            'mdo*': self.open_every_metadata_py,
            'mdw*': self.rewrite_every_metadata_py,
            #
            'nls*': self.list_every_init_py,
            'no*': self.open_every_init_py,
            'ns*': self.write_every_init_py_stub,
            })
        return result

    ### PRIVATE METHODS ###

    def _list_metadata_py_files_in_all_directories(self):
        paths = []
        directories = self._list_all_directories_with_metadata_pys()
        for directory in directories:
            path = os.path.join(directory, '__metadata__.py')
            paths.append(path)
        paths.sort()
        return paths

    ### PUBLIC METHODS ###

    def list_every_init_py(self):
        r'''Lists ``__init__.py`` in every package.

        Returns none.
        '''
        file_name = '__init__.py'
        paths = []
        for segment_path in self._list_visible_asset_paths():
            path = os.path.join(segment_path, file_name)
            if os.path.isfile(path):
                paths.append(path)
        if not paths:
            message = 'no {} files found.'
            message = message.format(file_name)
            self._io_manager._display(message)
            return
        messages = []
        for path in paths:
            message = '    ' + path
            messages.append(message)
        message = '{} {} files found.'
        message.format(len(paths), file_name)
        messages.append(message)
        self._io_manager._display(message)

    def list_every_metadata_py(self):
        r'''Lists ``__metadata__.py`` in every package.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        messages = paths[:]
        self._io_manager._display(messages)
        message = '{} __metadata__.py files found.'
        message = message.format(len(paths))
        self._io_manager._display(message)

    def open_every_init_py(self):
        r'''Opens ``__init__.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('__init__.py')

    def open_every_metadata_py(self):
        r'''Opens ``__metadata__.py`` in every package.

        Returns none.
        '''
        paths = self._list_metadata_py_files_in_all_directories()
        messages = []
        messages.append('will open ...')
        for path in paths:
            message = '    ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        self._io_manager.open_file(paths)

    def rewrite_every_metadata_py(self):
        r'''Rewrites ``__metadata__.py`` in every package.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        messages = []
        for directory in directories:
            path = os.path.join(directory, '__metadata__.py')
            message = 'rewriting {} ...'.format(path)
            messages.append(message)
            manager = self._io_manager._make_package_manager(directory)
            with self._io_manager._make_silent():
                manager.rewrite_metadata_py()
        message = '{} __metadata__.py files rewritten.'
        message = message.format(len(directories))
        messages.append(message)
        self._io_manager._display(messages)

    def write_every_init_py_stub(self):
        r'''Writes stub ``__init__.py`` in every package.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()