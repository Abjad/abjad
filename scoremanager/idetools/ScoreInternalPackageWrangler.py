# -*- encoding: utf-8 -*-
from scoremanager.idetools.PackageWrangler import PackageWrangler


class ScoreInternalPackageWrangler(PackageWrangler):
    r'''Score-internal package wrangler.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(ScoreInternalPackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'dc*': self.check_every_definition_py,
            'de*': self.edit_every_definition_py,
            #
            'ii*': self.interpret_every_illustration_ly,
            'io*': self.open_every_illustration_pdf,
            #
            'ne': self.edit_init_py,
            'nl': self.list_init_py,
            'ns': self.write_stub_init_py,
            #
            'vr*': self.version_every_package,
            'vl*': self.list_every_versions_directory,
            })
        return result

    ### PRIVATE METHODS ###

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        superclass = super(ScoreInternalPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('all packages - definition.py - check', 'dc*'))
        commands.append(('all packages - definition.py - edit', 'de*'))
        commands.append(('all packages - illustration.ly - interpret', 'ii*'))
        commands.append(('all packages - illustration.pdf - open', 'io*'))
        commands.append(('all packages - versions - list directory', 'vl*'))
        commands.append(('all packages - version', 'vr*'))
        if commands_only:
            return commands
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all packages',
            )

    def _make_main_menu(self):
        superclass = super(ScoreInternalPackageWrangler, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    # TODO: factor out check_every_output_py shared code
    def check_every_definition_py(self):
        r'''Checks ``definition.py`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'check_definition_py'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs, verb='check')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            method = getattr(manager, method_name)
            method()

    def edit_init_py(self):
        r'''Edits ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.edit_init_py()

    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    def interpret_every_illustration_ly(
        self, 
        open_every_illustration_pdf=True,
        ):
        r'''Interprets ``illustration.ly`` in every package.

        Makes ``illustration.pdf`` in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        inputs, outputs = [], []
        method_name = 'interpret_illustration_ly'
        for manager in managers:
            method = getattr(manager, method_name)
            inputs_, outputs_ = method(dry_run=True)
            inputs.extend(inputs_)
            outputs.extend(outputs_)
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in managers:
            with self._io_manager._silent():
                method = getattr(manager, method_name)
                subprocess_messages, candidate_messages = method()
            if subprocess_messages:
                self._io_manager._display(subprocess_messages)
                self._io_manager._display(candidate_messages)
                self._io_manager._display('')

    def list_every_versions_directory(self):
        r'''Lists versions directory in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        messages = []
        tab = self._io_manager._tab
        for manager in managers:
            string = self._path_to_asset_menu_display_string(manager._path)
            message = string + ':'
            messages.append(message)
            messages_ = manager.list_versions_directory(messages_only=True)
            messages_ = [tab + _ for _ in messages_]
            messages.extend(messages_)
        self._io_manager._display(messages)

    def list_init_py(self):
        r'''Lists ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.list_init_py()

    def version_every_package(self):
        r'''Versions every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        messages, refuse_messages = [], []
        for manager in managers:
            result, messages_ = manager._audit_version_differences()
            if result:
                messages.extend(messages_)
            else:
                refuse_messages.extend(messages_)
        if refuse_messages:
            refuse_messages.insert(0, 'nothing to version ...')
            refuse_messages.append('')
            self._io_manager._display(refuse_messages)
        if not messages:
            return
        messages.insert(0, 'will copy ...')
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in self._list_visible_asset_managers():
            with self._io_manager._silent():
                manager.version_package()

    def write_stub_init_py(self):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.write_stub_init_py()