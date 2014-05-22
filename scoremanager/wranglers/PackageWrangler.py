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
            #
            'cp': self.copy_package,
            'new': self.make_package,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            #
            'mdls*': self.list_every_metadata_py,
            'mdo*': self.open_every_metadata_py,
            'mdw*': self.rewrite_every_metadata_py,
            #
            'no*': self.open_every_init_py,
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

    def list_every_metadata_py(self):
        r'''Lists ``__metadata__.py`` in every package.

        Returns none.
        '''
        with self._io_manager._make_interaction():
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

    def open_every_metadata_py(self, confirm=True, display=True):
        r'''Opens ``__metadata__.py`` in every package.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            paths = self._list_metadata_py_files_in_all_directories()
            if display:
                messages = []
                messages.append('will open ...')
                for path in paths:
                    message = '    ' + path
                    messages.append(message)
                self._io_manager._display(messages)
            if confirm:
                result = self._io_manager._confirm()
                if self._session.is_backtracking:
                    return
                if not result:
                    return
            self._io_manager.open_file(paths)


    def rewrite_every_metadata_py(self, confirm=True, display=True):
        r'''Rewrites ``__metadata__.py`` in every package.

        Returns none.
        '''
        with self._io_manager._make_interaction(display=display):
            directories = self._list_all_directories_with_metadata_pys()
            messages = []
            for directory in directories:
                path = os.path.join(directory, '__metadata__.py')
                message = 'rewriting {} ...'.format(path)
                messages.append(message)
                manager = self._io_manager._make_package_manager(directory)
                manager.rewrite_metadata_py(confirm=False, display=False)
            if display:
                message = '{} __metadata__.py files rewritten.'
                message = message.format(len(directories))
                messages.append(message)
                self._session._hide_next_redraw = False
                self._io_manager._display(messages)