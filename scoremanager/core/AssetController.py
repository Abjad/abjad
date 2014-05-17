import os
from scoremanager.core.Controller import Controller


class AssetController(Controller):
    r'''Asset controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(AssetController, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'd': self.go_to_distribution_files,
            'g': self.go_to_segment_packages,
            'k': self.go_to_maker_files,
            'm': self.go_to_material_packages,
            'u': self.go_to_build_files,
            'y': self.go_to_stylesheets,
            #
            'ess': self.edit_score_stylesheet,
            #
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'rcn': self.repository_clean,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            })
        return result

    ### PRIVATE METHODS ###

    def _make_init_py_menu_section(self, menu):
        commands = []
        commands.append(('__init__.py - open', 'ipyo'))
        commands.append(('__init__.py - write stub', 'ipyws'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='__init__.py',
            )

    def _make_go_edits_menu_section(self, menu):
        commands = []
        commands.append(('edit - score stylesheet', 'ess'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='edit - zzz',
            )

    def _make_go_wranglers_menu_section(self, menu):
        commands = []
        commands.append(('go - build', 'u'))
        commands.append(('go - distribution', 'd'))
        commands.append(('go - makers', 'k'))
        commands.append(('go - materials', 'm'))
        commands.append(('go - segments', 'g'))
        commands.append(('go - stylesheets', 'y'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go - wranglers',
            )
            
    def _make_repository_menu_section(self, menu):
        commands = []
        commands.append(('repository - add', 'rad'))
        commands.append(('repository - clean', 'rcn'))
        commands.append(('repository - commit', 'rci'))
        commands.append(('repository - revert', 'rrv'))
        commands.append(('repository - status', 'rst'))
        commands.append(('repository - update', 'rup'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='repository',
            )

    def _open_file(self, path):
        with self._io_manager.make_interaction():
            if os.path.isfile(path):
                self._io_manager.open_file(path)
            else:
                message = 'can not find file: {}.'
                message = message.format(path)
                self._io_manager.display(message)

    def _repository_clean(self, confirm=True, display=True):
        with self._io_manager.make_interaction(display=display):
            paths = self._get_unadded_asset_paths()
            if not paths:
                if display:
                    message = 'no unadded assets.'
                    self._io_manager.display(message)
                return
            if display:
                messages = []
                messages.append('will remove ...')
                for path in paths:
                    message = '    ' + path
                    messages.append(message)
                self._io_manager.display(messages)
            if confirm:
                result = self._io_manager.confirm()
                if self._should_backtrack():
                    return
                if not result:
                    return
            remove_command = self._shell_remove_command
            paths = ' '.join(paths)
            command = '{} {}'
            command = command.format(remove_command, paths)
            self._io_manager.run_command(command)

    ### PUBLIC METHODS ###

    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        with self._io_manager.make_interaction():
            path = self._session.current_stylesheet_path
            if path:
                self._io_manager.edit(path)
            else:
                message = 'no file ending in *stylesheet.ily found.'
                self._io_manager.display(message)

    def go_to_build_files(self):
        r'''Goes to build files.

        Returns none.
        '''
        self._session._score_manager._build_file_wrangler._run()

    def go_to_distribution_files(self):
        r'''Goes to distribution files.

        Returns none.
        '''
        self._session._score_manager._distribution_file_wrangler._run()

    def go_to_maker_files(self):
        r'''Goes to maker files.

        Returns none.
        '''
        self._session._score_manager._maker_file_wrangler._run()

    def go_to_material_packages(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._score_manager._material_package_wrangler._run()

    def go_to_segment_packages(self):
        r'''Goes to segment packages.

        Returns none.
        '''
        self._session._score_manager._segment_package_wrangler._run()

    def go_to_stylesheets(self):
        r'''Goes to stylesheets.

        Returns none.
        '''
        self._session._score_manager._stylesheet_wrangler._run()