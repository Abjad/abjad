# -*- encoding: utf-8 -*-
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class ScoreInternalPackageWrangler(PackageWrangler):
    r'''Score-internal package wrangler.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(ScoreInternalPackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'nls': self.list_init_py,
            'no': self.open_init_py,
            'ns': self.write_stub_init_py,
            #
            'vr*': self.version_every_package,
            'vrls*': self.list_every_versions_directory,
            })
        return result

    ### PRIVATE METHODS ###

    def _make_all_packages_menu_section(self, menu, commands_only=False):
        superclass = super(ScoreInternalPackageWrangler, self)
        commands = superclass._make_all_packages_menu_section(
            menu, commands_only=True)
        commands.append(('all packages - versions - list directory', 'vrls*'))
        commands.append(('all packages - version', 'vr*'))
        if commands_only:
            return commands
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all packages',
            )

    ### PUBLIC METHODS ###

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

    def list_every_versions_directory(self):
        r'''Lists versions directory in every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        messages = []
        tab = self._io_manager._make_tab()
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

    def open_init_py(self):
        r'''Opens ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.open_init_py()

    def version_every_package(self):
        r'''Versions every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        messages = []
        messages.append('will copy ...')
        for manager in managers:
            messages.extend(manager._make_version_package_messages())
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        for manager in self._list_visible_asset_managers():
            with self._io_manager._make_silent():
                manager.version_package()

    def write_stub_init_py(self):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        self._current_package_manager.write_stub_init_py()