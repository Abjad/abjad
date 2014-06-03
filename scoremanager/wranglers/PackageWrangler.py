# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
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
            'ck*': self.check_every_package,
            'fix*': self.fix_every_package,
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

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        commands = []
        commands.append(('all packages - __init__.py - list', 'nls*'))
        commands.append(('all packages - __init__.py - open', 'no*'))
        commands.append(('all packages - __init__.py - stub', 'ns*'))
        commands.append(('all packages - __metadata__.py - list', 'mdls*'))
        commands.append(('all packages - __metadata__.py - open', 'mdo*'))
        commands.append(('all packages - __metadata__.py - rewrite', 'mdw*'))
        commands.append(('all packages - check', 'ck*'))
        commands.append(('all packages - fix', 'fix*'))
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
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return
            problems_only = bool(result)
        managers = self._list_visible_asset_managers()
        messages = []
        path = self._get_current_directory()
        name = os.path.basename(path)
        count = len(managers)
        message = '{} ({} packages):'.format(name, count)
        messages.append(message)
        first_tab = self._io_manager._make_tab(indent)
        second_tab = self._io_manager._make_tab(indent+1)
        found_problem = False
        for manager in managers:
            messages_ = manager.check_package(
                return_messages=True,
                problems_only=problems_only,
                )
            messages_ = [stringtools.capitalize_start(_) for _ in messages_]
            messages_ = [first_tab + _ for _ in messages_]
            if messages_:
                found_problem = True
                messages.extend(messages_)
            else:
                message = 'No problem assets found.'
                message = second_tab + message
                messages.append(message)
        self._io_manager._display(messages)
        if not found_problem:
            return
        if supply_missing is None:
            prompt = 'supply missing directories and files?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return
            supply_missing = bool(result)
        if not supply_missing:
            return
        messages = []
        for path in paths:
            manager = self._initialize_manager(path)
            with self._io_manager._make_silent():
                messages_ = manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
            if messages_:
                name = self._path_to_asset_menu_display_string(manager._path)
                message = '{} ({} packages):'.format(name, count)
                message = first_tab + message
                messages.append(message)
                messages_ = [stringtools.capitalize_start(_) for _ in messages_] 
                messages_ = [second_tab + _ for _ in messages_]
                messages.extend(messages_)
        self._io_manager._display(messages)

    def fix_every_package(self):
        r'''Fixes every package.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        messages = []
        for path in paths:
            manager = self._initialize_manager(path)
            needed_to_be_fixed = manager.fix_package()
            if not needed_to_be_fixed:
                if hasattr(manager, '_get_title'):
                    title = manager._get_title()
                else:
                    title = manager._package_name
                message = '{} OK.'
                message = message.format(title)
                messages.append(message)
        message = '{} packages checked.'
        message = message.format(len(paths))
        messages.append(message)
        self._io_manager._display(messages)

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
        if self._session.is_backtracking or not result:
            return
        self._io_manager.open_file(paths)

    def rewrite_every_metadata_py(self):
        r'''Rewrites ``__metadata__.py`` in every package.

        Returns none.
        '''
        directories = self._list_all_directories_with_metadata_pys()
        managers = []
        for directory in directories:
            manager = self._io_manager._make_package_manager(directory)
            managers.append(manager)
        inputs, outputs = [], []
        for manager in managers:
            inputs_, outputs_ = manager.rewrite_metadata_py(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(
            inputs, 
            outputs, 
            verb='rewrite',
            )
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        with self._io_manager._make_silent():
            for manager in managers:
                manager.rewrite_metadata_py()
        message = '{} __metadata__.py files rewritten.'
        message = message.format(len(managers))
        self._io_manager._display(message)

    def write_every_init_py_stub(self):
        r'''Writes stub ``__init__.py`` in every package.

        Returns none.
        '''
        self._io_manager._display_not_yet_implemented()