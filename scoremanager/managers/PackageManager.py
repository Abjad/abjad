# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.managers.DirectoryManager import DirectoryManager


class PackageManager(DirectoryManager):
    r'''Package manager.
    '''

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
    def _initializer_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )

    @property
    def _initializer_file_path(self):
        if self._path is not None:
            return os.path.join(self._path, '__init__.py')

#    @property
#    def _metadata_module_path(self):
#        file_path = os.path.join(self._path, '__metadata__.py')
#        return file_path

    @property
    def _space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            result = base_name.replace('_', ' ')
            return result

    @property
    def _user_input_to_action(self):
        superclass = super(PackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'inrm': self.remove_initializer,
            'ins': self.write_initializer_stub,
            'inro': self.view_initializer,
            'ren': self.rename,
            'rm': self.remove,
            })
        return result

    @property
    def _views_module_path(self):
        file_path = os.path.join(self._path, '__views__.py')
        return file_path

    ### PRIVATE METHODS ###

    def _make_main_menu(self, where=None, name='package manager'):
        where = where or self._where
        menu = self._io_manager.make_menu(
            where=where,
            name=name,
            )
        return menu

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    ### PUBLIC METHODS ###

    def remove_initializer(self, prompt=True):
        r'''Removes initializer module.

        Returns none.
        '''
        if os.path.isfile(self._initializer_file_path):
            os.remove(self._initializer_file_path)
            line = 'initializer deleted.'
            self._io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def remove_views_module(self, prompt=True):
        r'''Removes views module.

        Returns none.
        '''
        if os.path.isfile(self._views_module_path):
            if prompt:
                message = 'remove views module?'
                if not self._io_manager.confirm(message):
                    return
            os.remove(self._views_module_path)
            line = 'views module removed.'
            self._io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def rename(self):
        r'''Renames package.

        Returns none.
        '''
        base_name = os.path.basename(self._path)
        line = 'current name: {}'.format(base_name)
        self._io_manager.display(line)
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self._session._backtrack():
            return
        lines = []
        line = 'current name: {}'.format(base_name)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        lines.append('')
        self._io_manager.display(lines)
        if not self._io_manager.confirm():
            return
        new_directory_path = self._path.replace(
            base_name,
            new_package_name,
            )
        if self._is_svn_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self._path, new_directory_path)
            self._io_manager.spawn_subprocess(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory_path = os.path.dirname(self._path)
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                parent_directory_path,
                )
            self._io_manager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self._path, new_directory_path)
            self._io_manager.spawn_subprocess(command)
        # update path name to reflect change
        self._path = new_directory_path
        self._session._is_backtracking_locally = True

    def view_initializer(self):
        r'''Views initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager.view()

    def write_initializer_boilerplate(self, prompt=True):
        r'''Writes boilerplate initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager.write_boilerplate(prompt=prompt)

    def write_initializer_stub(self, prompt=True):
        r'''Wrties stub initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager._write_stub()
        message = 'stub initializer written.'
        self._io_manager.proceed(message)