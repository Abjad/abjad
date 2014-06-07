import collections
import os
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class AssetController(Controller):
    r'''Asset controller.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_annotate_year',
        '_human_readable',
        '_include_asset_name',
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):                                           
        superclass = super(AssetController, self)                                    
        superclass.__init__(session=session)                                    
        self._annotate_year = False
        self._human_readable = True
        self._include_asset_name = True
        self._include_extensions = False

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(AssetController, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            '<<': self.go_to_previous_score,
            '>>': self.go_to_next_score,
            #
            '**': self.go_to_library,
            'd': self.go_to_distribution_files,
            'g': self.go_to_segments,
            'k': self.go_to_maker_files,
            'm': self.go_to_materials,
            'u': self.go_to_build_files,
            'y': self.go_to_stylesheets,
            #
            'cc': self.check_contents,
            #
            'mdo': self.open_metadata_py,
            'mdls': self.list_metadata_py,
            'mdw': self.write_metadata_py,
            #
            'sse': self.edit_score_stylesheet,
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

    @property
    def _navigation_commands(self):
        return (
            '**', 'd', 'g', 'k', 'm', 'u', 'y',
            'b', 's', 'h', 'q',
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _format_messaging(inputs, outputs, verb='interpret'):
        messages = []
        if not inputs and not outputs:
            message = 'no files to {}.'
            message = message.format(verb)
            messages.append(message)
            return messages
        message = 'will {} ...'.format(verb)
        messages.append(message)
        if outputs:
            input_label = '  INPUT: '
        else:
            input_label = '    '
        output_label = ' OUTPUT: '
        if not outputs:
            for path_list in inputs:
                if isinstance(path_list, str):
                    path_list = [path_list]
                for path in path_list:
                    messages.append('{}{}'.format(input_label, path))
        else:
            for inputs_, outputs_ in zip(inputs, outputs):
                if isinstance(inputs_, str):
                    inputs_ = [inputs_]
                assert isinstance(inputs_, (tuple, list)), repr(inputs_)
                for path_list in inputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(input_label, path))
                for path_list in outputs_:
                    if isinstance(path_list, str):
                        path_list = [path_list]
                    for path in path_list:
                        messages.append('{}{}'.format(output_label, path))
        return messages

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_py_path):
            with open(self._metadata_py_path, 'r') as file_pointer:
                file_contents_string = file_pointer.read()
            try:
                local_dict = {}
                exec(file_contents_string, globals(), local_dict)
                metadata = local_dict.get('metadata')
            except:
                message = 'can not interpret metadata py: {!r}.'
                message = message.format(self)
                self._io_manager._display(message)
        metadata = metadata or collections.OrderedDict()
        return metadata

    def _go_to_next_package(self):
        self._session._is_navigating_to_next_asset = True
        self._session._hide_available_commands = True
        self._set_is_navigating_to_sibling_asset()

    def _go_to_previous_package(self):
        self._session._is_navigating_to_previous_asset = True
        self._session._hide_available_commands = True
        self._set_is_navigating_to_sibling_asset()

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            return
        with self._io_manager._make_interaction():
            if result.startswith('!'):
                statement = result[1:]
                self.invoke_shell(statement=statement)
            elif result in self._input_to_method:
                self._input_to_method[result]()
            else:
                self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        pass

    def _make_go_menu_section(self, menu, packages=False):
        commands = []
        commands.append(('go - back', 'b'))
        commands.append(('go - home', 'h'))
        commands.append(('go - library', '**'))
        commands.append(('go - quit', 'q'))
        commands.append(('go - score', 's'))
        if packages:
            commands.append(('go - next package', '>'))
            commands.append(('go - previous package', '<'))
        commands.append(('go - next score', '>>'))
        commands.append(('go - previous score', '<<'))
        commands.append(('go - build', 'u'))
        commands.append(('go - distribution', 'd'))
        commands.append(('go - makers', 'k'))
        commands.append(('go - materials', 'm'))
        commands.append(('go - segments', 'g'))
        commands.append(('go - stylesheets', 'y'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='go',
            )

    def _make_init_py_menu_section(self, menu):
        commands = []
        commands.append(('__init__.py - list', 'nls'))
        commands.append(('__init__.py - open', 'no'))
        commands.append(('__init__.py - stub', 'ns'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='__init__.py',
            )

    def _make_main_menu(self):
        name = self._spaced_class_name
        menu = self._io_manager._make_menu(name=name)
        if self._session.is_in_score:
            self._make_score_stylesheet_menu_section(menu)
        self._make_go_menu_section(menu)
        self._make_repository_menu_section(menu)
        self._make_system_menu_section(menu)
        return menu
            
    @staticmethod
    def _make_metadata_lines(metadata):
        if metadata:
            lines = []
            for key, value in sorted(metadata.items()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = \
                        value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    if hasattr(value, '_storage_format_specification'):
                        string = format(value)
                    else:
                        string = repr(value)
                    lines.append('({}, {})'.format(key, string))
            lines = ',\n    '.join(lines)
            result = 'metadata = collections.OrderedDict([\n    {},\n    ])'
            result = result.format(lines)
        else:
            result = 'metadata = collections.OrderedDict([])'
        return result

    def _make_metadata_menu_section(self, menu):
        commands = []
        commands.append(('metadata - add', 'mda'))
        commands.append(('metadata - get', 'mdg'))
        commands.append(('metadata - remove', 'mdrm'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadata',
            )
            
    def _make_metadata_py_menu_section(self, menu):
        commands = []
        commands.append(('__metadata__.py - list', 'mdls'))
        commands.append(('__metadata__.py - open', 'mdo'))
        commands.append(('__metadata__.py - rewrite', 'mdw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='__metadata__.py',
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

    def _make_score_stylesheet_menu_section(self, menu):
        commands = []
        commands.append(('score stylesheet - edit', 'sse'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='score stylesheet',
            )

    def _make_sibling_asset_tour_menu_section(self, menu):
        section = menu['go']
        menu.menu_sections.remove(section)
        self._make_go_menu_section(menu, packages=True)

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
        if os.path.isfile(path):
            self._io_manager.open_file(path)
        else:
            message = 'can not find file: {}.'
            message = message.format(path)
            self._io_manager._display(message)

    def _path_to_annotation(self, path):
        score_storehouses = (
            self._configuration.example_score_packages_directory,
            self._configuration.user_score_packages_directory,
            )
        if path.startswith(score_storehouses):
            score_path = self._configuration._path_to_score_path(path)
            manager = self._io_manager._make_package_manager(path=score_path)
            metadata = manager._get_metadata()
            if metadata:
                year = metadata.get('year')
                title = metadata.get('title')
                if self._annotate_year and year:
                    annotation = '{} ({})'.format(title, year)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = package_name
        #elif (hasattr(self, '_user_storehouse_path') and
        #    path.startswith(self._user_storehouse_path)):
        elif path.startswith(self._configuration.user_library_directory):
            annotation = self._configuration.composer_last_name
        #elif (hasattr(self, '_abjad_storehouse_path') and
        #    path.startswith(self._abjad_storehouse_path)):
        elif path.startswith(self._configuration.abjad_root_directory):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    def _path_to_asset_menu_display_string(self, path):
        if self._human_readable:
            asset_name = self._path_to_human_readable_name(path)
        else:
            asset_name = os.path.basename(path)
        if 'segments' in path:
            manager = self._io_manager._make_package_manager(path=path)
            name = manager._get_metadatum('name')
            asset_name = name or asset_name
        if self._session.is_in_score:
            string = asset_name
        else:
            annotation = self._path_to_annotation(path)
            if self._include_asset_name:
                string = '{} ({})'.format(asset_name, annotation)
            else:
                string = annotation
        if getattr(self, '_annotate_autoeditor', False):
            use_autoeditor = False
            manager = self._io_manager._make_package_manager(path=path)
            metadata = manager._get_metadata()
            if metadata:
                use_autoeditor = metadata.get('use_autoeditor')
            if use_autoeditor:
                string = string + ' (AE)'
        return string

    def _path_to_human_readable_name(self, path):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        include_extensions = self._include_extensions
        if not include_extensions:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    def _repository_clean(self):
        paths = self._get_unadded_asset_paths()
        if not paths:
            message = 'no unadded assets.'
            self._io_manager._display(message)
            return
        messages = []
        messages.append('will remove ...')
        for path in paths:
            message = '    ' + path
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        remove_command = self._shell_remove_command
        paths = ' '.join(paths)
        command = '{} {}'
        command = command.format(remove_command, paths)
        self._io_manager.run_command(command)

    def _write_metadata_py(self, metadata):
        lines = []
        lines.append(self._configuration.unicode_directive)
        lines.append('import collections')
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        metadata_lines = self._make_metadata_lines(metadata)
        contents = contents + '\n' + metadata_lines
        with open(self._metadata_py_path, 'w') as file_pointer:
            file_pointer.write(contents)

    ### PUBLIC METHODS ###

    def check_contents(self):
        r'''Checks contents.

        Returns none.
        '''
        pass

    def display_available_commands(self):
        r'''Displays available commands.

        Returns none.
        '''
        if (not self._session.is_in_confirmation_environment and
            not self._session.is_in_autoeditor):
            hide = self._session.hide_available_commands
            self._session._hide_available_commands = not hide

    def display_session_variables(self):
        r'''Displays session variables.

        Returns none.
        '''
        self._session._display_variables()

    def doctest(self):
        r'''Doctests Python files.
        
        Returns none.
        '''
        message = 'running doctest ...'
        self._io_manager._display(message)
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
            self._io_manager._display(message)
        else:
            count = len(assets)
            identifier = stringtools.pluralize('asset', count=count)
            message = '{} testable {} found ...'
            message = message.format(count, identifier)
            self._io_manager._display(message)
            script = developerscripttools.RunDoctestsScript()
            strings = script.process_args(
                file_paths=assets,
                print_to_terminal=False,
                )
            self._io_manager._display(strings, capitalize=False)

    def edit_score_stylesheet(self):
        r'''Edits score stylesheet.

        Returns none.
        '''
        path = self._session.current_stylesheet_path
        if path:
            self._io_manager.edit(path)
        else:
            message = 'no file ending in *stylesheet.ily found.'
            self._io_manager._display(message)

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

    def go_to_materials(self):
        r'''Goes to material packages.

        Returns none.
        '''
        self._session._score_manager._material_package_wrangler._run()

    def go_to_next_score(self):
        r'''Goes to next score.

        Returns none.
        '''
        self._session._is_navigating_to_next_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_available_commands = True

    def go_to_previous_score(self):
        r'''Goes to previous score.

        Returns none.
        '''
        self._session._is_navigating_to_previous_score = True
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_available_commands = True

    def go_to_segments(self):
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
            self._io_manager._display(messages)

    def invoke_shell(self, statement=None):
        r'''Invokes shell on `statement`.

        Returns none.
        '''
        self._io_manager.invoke_shell(statement=statement)

    def list_metadata_py(self):
        r'''Lists ``__metadata__.py``.

        Returns none.
        '''
        self._io_manager._display(self._metadata_py_path)

    def open_lilypond_log(self):
        r'''Opens LilyPond log.

        Returns none.
        '''
        from abjad.tools import systemtools
        self._session._attempted_to_open_file = True
        if self._session.is_test:
            return
        systemtools.IOManager.open_last_log()

    def open_metadata_py(self):
        r'''Opens ``__metadata__.py``.

        Returns none.
        '''
        self._open_file(self._metadata_py_path)

    def pytest(self):
        r'''Pytests Python files.

        Returns none.
        '''
        message = 'running py.test ...'
        self._io_manager._display(message)
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
            self._io_manager._display(message)
        else:
            count = len(paths)
            identifier = stringtools.pluralize('asset', count=count)
            message = '{} testable {} found ...'
            message = message.format(count, identifier)
            self._io_manager._display(message)
            assets = ' '.join(assets)
            command = 'py.test -rf {}'.format(assets)
            self._io_manager.run_command(command, capitalize=False)

    def write_metadata_py(self, dry_run=False, metadata=None):
        r'''Writes ``__metadata.py__``.

        Returns none.
        '''
        inputs, outputs = [], []
        inputs.append(self._metadata_py_path)
        if dry_run:
            return inputs, outputs
        messages = self._format_messaging(inputs, outputs, verb='rewrite')
        self._io_manager._display(messages)
        # WEIRD: why can't this confirm check be removed?
        if self._session.confirm:
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
        if metadata is None:
            metadata = self._get_metadata()
        self._write_metadata_py(metadata)