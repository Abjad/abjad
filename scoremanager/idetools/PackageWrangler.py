# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from scoremanager.idetools.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(PackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_package,
            'new': self.make_package,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            #
            'ck*': self.check_every_package,
            #
            'mdl*': self.list_every_metadata_py,
            'mde*': self.edit_every_metadata_py,
            'mdw*': self.write_every_metadata_py,
            #
            'nl*': self.list_every_init_py,
            'ne*': self.edit_every_init_py,
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

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        commands = []
        commands.append(('all packages - __init__.py - edit', 'ne*'))
        commands.append(('all packages - __init__.py - list', 'nl*'))
        commands.append(('all packages - __init__.py - stub', 'ns*'))
        commands.append(('all packages - __metadata__.py - edit', 'mde*'))
        commands.append(('all packages - __metadata__.py - list', 'mdl*'))
        commands.append(('all packages - __metadata__.py - write', 'mdw*'))
        commands.append(('all packages - check', 'ck*'))
        commands.append(('all packages - repository - add', 'rad*'))
        commands.append(('all packages - repository - clean', 'rcn*'))
        commands.append(('all packages - repository - commit', 'rci*'))
        commands.append(('all packages - repository - revert', 'rrv*'))
        commands.append(('all packages - repository - status', 'rst*'))
        commands.append(('all packages - repository - update', 'rup*'))
        if commands_only:
            return commands
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='all packages',
            )

    ### PUBLIC METHODS ###

    def check_every_package(
        self, 
        indent=0,
        problems_only=None, 
        supply_missing=None,
        ):
        r'''Checks every package.

        Returns none.
        '''
        messages = []
        missing_directories, missing_files = [], []
        supplied_directories, supplied_files = [], []
        tab = indent * self._io_manager._tab
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            problems_only = bool(result)
        managers = self._list_visible_asset_managers()
        found_problem = False
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_messages=True,
                    problems_only=problems_only,
                    )
            messages_, missing_directories_, missing_files_ = result
            missing_directories.extend(missing_directories_)
            missing_files.extend(missing_files_)
            messages_ = [stringtools.capitalize_start(_) for _ in messages_]
            messages_ = [tab + _ for _ in messages_]
            if messages_:
                found_problem = True
                messages.extend(messages_)
            else:
                message = 'No problem assets found.'
                message = tab + tab + message
                messages.append(message)
        found_problems = bool(messages)
        if self._session.is_in_score:
            path = self._get_current_directory()
            name = os.path.basename(path)
            count = len(managers)
            message = '{} directory ({} packages):'.format(name, count)
            if not found_problems:
                message = '{} OK'.format(message)
            messages.insert(0, message)
        self._io_manager._display(messages)
        if not found_problem:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            prompt = 'supply missing directories and files?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
            messages_, supplied_directories_, supplied_files_ = result
            supplied_directories.extend(supplied_directories_)
            supplied_files.extend(supplied_files_)
            if messages_:
                messages_ = [tab + tab + _ for _ in messages_]
                messages.extend(messages_)
        self._io_manager._display(messages)
        return messages, supplied_directories, supplied_files

    def edit_every_init_py(self):
        r'''Opens ``__init__.py`` in every package.

        Returns none.
        '''
        self._open_in_every_package('__init__.py')

    def edit_every_metadata_py(self):
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
        if self._session.is_backtracking or not result:
            return
        self._io_manager.open_file(paths)

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

    def make_package(self):
        r'''Makes package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._user_storehouse_path
        path = self._get_available_path(storehouse_path=storehouse_path)
        if self._session.is_backtracking or not path:
            return
        message = 'path will be {}.'.format(path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        manager = self._get_manager(path)
        manager._make_package()
        paths = self._list_visible_asset_paths()
        if path not in paths:
            with self._io_manager._silent():
                self._clear_view()
        if hasattr(self, 'write_cache'):
            self.write_cache()
        manager._run()

    def write_every_init_py_stub(self):
        r'''Writes stub ``__init__.py`` in every package.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()

    def write_every_metadata_py(self):
        r'''Rewrites ``__metadata__.py`` in every package.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        managers = []
        for directory in directories:
            manager = self._io_manager._make_package_manager(directory)
            managers.append(manager)
        inputs, outputs = [], []
        method_name = 'write_metadata_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(
            inputs, 
            outputs, 
            verb='write',
            )
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._silent():
            for manager in managers:
                method = getattr(manager, method_name)
                method()
        message = '{} __metadata__.py files rewritten.'
        message = message.format(len(managers))
        self._io_manager._display(message)