import os
from abjad.tools import developerscripttools
from abjad.tools import stringtools
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
            '<': self.go_to_previous_asset,
            '>': self.go_to_next_asset,
            '<<': self.go_to_previous_score,
            '>>': self.go_to_next_score,
            #
            'd': self.go_to_distribution_files,
            'g': self.go_to_segment_packages,
            'k': self.go_to_maker_files,
            'm': self.go_to_material_packages,
            'u': self.go_to_build_files,
            'y': self.go_to_stylesheets,
            #
            'ess': self.edit_score_stylesheet,
            #
            '!': self.invoke_shell,
            '?': self.display_available_commands,
            'log': self.open_lilypond_log,
            'pyd': self.doctest,
            'pyi': self.invoke_python,
            'pyt': self.pytest,
            'sv': self.display_session_variables,
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

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str), repr(result)
        if result == 'user entered lone return':
            pass
        elif result.startswith('!'):
            statement = result[1:]
            self.invoke_shell(statement=statement)
        elif result in self._input_to_method:
            self._input_to_method[result]()
        else:
            self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        pass

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

    def _make_go_menu_section(self, menu):
        commands = []
        commands.append(('go - back', 'b'))
        commands.append(('go - home', 'h'))
        commands.append(('go - quit', 'q'))
        commands.append(('go - score', 's'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go',
            )

    def _make_go_scores_menu_section(self, menu):
        commands = []
        commands.append(('go - next score', '>>'))
        commands.append(('go - previous score', '<<'))
        menu.make_command_section(
            is_alphabetized=False,
            is_hidden=True,
            commands=commands,
            name='go - scores',
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

    def _make_main_menu(self):
        name = self._spaced_class_name
        menu = self._io_manager.make_menu(name=name)
        if self._session.is_in_score:
            self._make_go_edits_menu_section(menu)
        self._make_go_menu_section(menu)
        self._make_go_wranglers_menu_section(menu)
        self._make_go_scores_menu_section(menu)
        self._make_repository_menu_section(menu)
        self._make_system_menu_section(menu)
        return menu
            
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

    def _make_sibling_asset_tour_menu_section(self, menu):
        section = menu['go - scores']
        menu.menu_sections.remove(section)
        commands = []
        commands.append(('go - next score', '>>'))
        commands.append(('go - next asset', '>'))
        commands.append(('go - previous score', '<<'))
        commands.append(('go - previous asset', '<'))
        menu.make_command_section(
            is_alphabetized=False,
            is_hidden=True,
            commands=commands,
            name='go - scores',
            )

    def _make_system_menu_section(self, menu):
        commands = []
        commands.append(('system - available commands', '?'))
        commands.append(('system - doctest', 'pyd'))
        commands.append(('system - session variables', 'sv'))
        commands.append(('system - LilyPond log', 'log'))
        commands.append(('system - Python', 'pyi'))
        commands.append(('system - pytest', 'pyt'))
        commands.append(('system - shell', '!'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='system', 
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
                if self._session.is_backtracking:
                    return
                if not result:
                    return
            remove_command = self._shell_remove_command
            paths = ' '.join(paths)
            command = '{} {}'
            command = command.format(remove_command, paths)
            self._io_manager.run_command(command)

    ### PUBLIC METHODS ###

    def display_available_commands(self):
        r'''Displays available commands.

        Returns none.
        '''
        if (not self._session.is_in_confirmation_environment and
            not self._session.is_in_editor):
            hide = self._session.hide_hidden_commands
            self._session._hide_hidden_commands = not hide

    def display_session_variables(self):
        r'''Displays session variables.

        Returns none.
        '''
        self._session._display_variables()

    def doctest(self):
        r'''Runs doctest on Python files contained in assets.
        
        Returns none.
        '''
        with self._io_manager.make_interaction():
            message = 'running doctest ...'
            self._io_manager.display(message)
            assets = []
            paths = self._list_visible_asset_paths()
            for path in paths:
                if path.endswith('.py'):
                    assets.append(path)
                if os.path.isdir(path):
                    triples = os.walk(path)
                    for directory_name, subdirectories, file_names in triples:
                        for file_name in file_names:
                            if file_name.endswith('.py'):
                                file_path = os.path.join(
                                    directory_name, 
                                    file_name,
                                    )
                                assets.append(file_path)
            if not assets:
                message = 'no testable assets found.'
                self._io_manager.display(message)
            else:
                count = len(assets)
                identifier = stringtools.pluralize('asset', count=count)
                message = '{} testable {} found ...'
                message = message.format(count, identifier)
                self._io_manager.display([message, ''])
                script = developerscripttools.RunDoctestsScript()
                strings = script.process_args(
                    file_paths=assets,
                    print_to_terminal=False,
                    )
                self._io_manager.display(strings, capitalize=False)

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

    def go_to_next_asset(self):
        r'''Goes to next asset.

        Returns none.
        '''
        self._session._is_navigating_to_next_asset = True
        self._session._hide_hidden_commands = True
        self._set_is_navigating_to_sibling_asset()

    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

    def go_to_previous_asset(self):
        r'''Goes to previous asset.

        Returns none.
        '''
        self._session._is_navigating_to_previous_asset = True
        self._session._hide_hidden_commands = True
        self._set_is_navigating_to_sibling_asset()

    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

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

    def invoke_python(self, statement=None):
        r'''Invokes Python on `statement`.

        Returns none.
        '''
        with self._io_manager.make_interaction():
            messages = []
            prompt = True
            if statement is None:
                statement = self._io_manager._handle_input(
                    '>>', 
                    include_newline=False,
                    )
            else:
                prompt = False
            command = 'from abjad import *'
            exec(command)
            try:
                result = None
                command = 'result = {}'.format(statement)
                exec(command)
                messages.append('{!r}'.format(result))
            except:
                messages.append('expression not executable.')
            if prompt:
                self._io_manager.display(messages)

    def invoke_shell(self, statement=None):
        r'''Invokes shell on `statement`.

        Returns none.
        '''
        self._io_manager.invoke_shell(statement=statement)

    def open_lilypond_log(self):
        r'''Opens last LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        with self._io_manager.make_interaction():
            self._session._attempted_to_open_file = True
            if self._session.is_test:
                return
            systemtools.IOManager.open_last_log()

    def pytest(self):
        r'''Runs py.test on Python files contained in visible assets.

        Returns none.
        '''
        with self._io_manager.make_interaction():
            message = 'running py.test ...'
            self._io_manager.display(message)
            assets = []
            paths = self._list_python_files_in_visible_assets()
            for path in paths:
                assert os.path.isfile(path)
            paths = [
                _ for _ in paths if os.path.basename(_).startswith('test_')
                ]
            for path in paths:
                if os.path.isdir(path):
                    assets.append(path)
                elif os.path.isfile(path) and path.endswith('.py'):
                    assets.append(path)
            if not assets:
                message = 'no testable assets found.'
                self._io_manager.display(message)
            else:
                count = len(paths)
                identifier = stringtools.pluralize('asset', count=count)
                message = '{} testable {} found ...'
                message = message.format(count, identifier)
                self._io_manager.display(message)
                assets = ' '.join(assets)
                command = 'py.test -rf {}'.format(assets)
                self._io_manager.run_command(command, capitalize=False)