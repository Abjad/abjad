# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.idetools.Controller import Controller


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
            '**': self.go_to_top_level,
            #
            'D': self.go_to_all_distribution_files,
            'G': self.go_to_all_segments,
            'K': self.go_to_all_maker_files,
            'M': self.go_to_all_materials,
            'U': self.go_to_all_build_files,
            'Y': self.go_to_all_stylesheets,
            #
            'cc': self.check_contents,
            #
            'mdo': self.open_metadata_py,
            'mdls': self.list_metadata_py,
            'mdw': self.write_metadata_py,
            #
            '!': self.invoke_shell,
            '??': self.display_available_commands,
            'log': self.open_lilypond_log,
            'pyd': self.doctest,
            'pyi': self.invoke_python,
            'pyt': self.pytest,
            'sv': self.display_session_variables,
            })
        return result

    @property
    def _navigation_commands(self):
        return (
            'b', 'q',
            '**', 'D', 'G', 'K', 'M', 'S', 'U', 'Y',
            )

    @property
    def _views_package_manager(self):
        path = self._configuration.wrangler_views_directory
        return self._io_manager._make_package_manager(path)

    ### PRIVATE METHODS ###

    def _filter_asset_menu_entries_by_view(self, entries):
        view = self._read_view()
        if view is None:
            return entries
        entries = entries[:]
        filtered_entries = []
        for pattern in view:
            if ':ds:' in pattern:
                for entry in entries:
                    if self._match_display_string_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            elif 'md:' in pattern:
                for entry in entries:
                    if self._match_metadata_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            elif ':path:' in pattern:
                for entry in entries:
                    if self._match_path_view_pattern(pattern, entry):
                        filtered_entries.append(entry)
            else:
                for entry in entries:
                    display_string, _, _, path = entry
                    if pattern == display_string:
                        filtered_entries.append(entry)
        return filtered_entries

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

    def _get_current_directory(self):
        score_directory = self._session.current_score_directory
        if score_directory is not None:
            parts = (score_directory,)
            parts += self._score_storehouse_path_infix_parts
            directory = os.path.join(*parts)
            assert '.' not in directory, repr(directory)
            return directory

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
        self._session._display_available_commands = False
        self._set_is_navigating_to_sibling_asset()

    def _go_to_previous_package(self):
        self._session._is_navigating_to_previous_asset = True
        self._session._display_available_commands = False
        self._set_is_navigating_to_sibling_asset()

    def _handle_input(self, result):
        assert isinstance(result, str), repr(result)
        if result == '<return>':
            return
        with self._io_manager._make_interaction():
            if result.startswith('!'):
                statement = result[1:]
                self._io_manager._invoke_shell(statement)
            elif result in self._input_to_method:
                self._input_to_method[result]()
            elif result.endswith('!') and result[:-1] in self._input_to_method:
                result = result[:-1]
                with self._io_manager._make_interaction(confirm=False):
                    self._input_to_method[result]()
            else:
                self._handle_numeric_user_input(result)

    def _handle_numeric_user_input(self, result):
        pass

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry[0].isalpha():
            if not directory_entry.endswith('.pyc'):
                return True
        return False

    def _make_asset_menu_entries(
        self,
        apply_current_directory=True,
        set_view=True,
        ):
        paths = self._list_asset_paths()
        current_directory = self._get_current_directory()
        if (apply_current_directory or set_view) and current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        strings = [self._path_to_asset_menu_display_string(_) for _ in paths]
        pairs = list(zip(strings, paths))
        if not self._session.is_in_score and self._sort_by_annotation:
            def sort_function(pair):
                string = pair[0]
                if '(' not in string:
                    return string
                open_parenthesis_index = string.find('(')
                assert string.endswith(')')
                annotation = string[open_parenthesis_index:]
                annotation = annotation.replace("'", '')
                annotation = stringtools.strip_diacritics(annotation)
                return annotation
            pairs.sort(key=lambda _: sort_function(_))
        else:
            def sort_function(pair):
                string = pair[0]
                string = stringtools.strip_diacritics(string)
                string = string.replace("'", '')
                return string
            pairs.sort(key=lambda _: sort_function(_))
        entries = []
        for string, path in pairs:
            entry = (string, None, None, path)
            entries.append(entry)
        if set_view and not self._session.is_test:
            entries = self._filter_asset_menu_entries_by_view(entries)
        if self._session.is_test:
            if getattr(self, '_only_example_scores_during_test', False):
                entries = [_ for _ in entries if 'Example Score' in _[0]]
        return entries

    def _make_asset_menu_section(self, menu):
        menu_entries = self._make_asset_menu_entries()
        if menu_entries:
            menu.make_asset_section(menu_entries=menu_entries)

    def _make_go_menu_section(self, menu, packages=False):
        commands = []
        commands.append(('go - all', '**'))
        commands.append(('go - all - build', 'U'))
        commands.append(('go - all - distribution', 'D'))
        commands.append(('go - all - makers', 'K'))
        commands.append(('go - all - materials', 'M'))
        commands.append(('go - all - scores', 'S'))
        commands.append(('go - all - segments', 'G'))
        commands.append(('go - all - stylesheets', 'Y'))
        if self._session.is_in_score:
            commands.append(('go - score', 's'))
            commands.append(('go - score - build', 'u'))
            commands.append(('go - score - distribution', 'd'))
            commands.append(('go - score - makers', 'k'))
            commands.append(('go - score - materials', 'm'))
            commands.append(('go - score - segments', 'g'))
            commands.append(('go - score - stylesheets', 'y'))
        commands.append(('go - system - back', 'b'))
        commands.append(('go - system - quit', 'q'))
        if packages:
            commands.append(('go - system - next package', '>'))
            commands.append(('go - system - previous package', '<'))
        commands.append(('go - system - next score', '>>'))
        commands.append(('go - system - previous score', '<<'))
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
        #self._make_repository_menu_section(menu)
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
        commands.append(('__metadata__.py - list', 'mdls'))
        commands.append(('__metadata__.py - open', 'mdo'))
        commands.append(('__metadata__.py - write', 'mdw'))
        commands.append(('metadata - add', 'mda'))
        commands.append(('metadata - get', 'mdg'))
        commands.append(('metadata - remove', 'mdrm'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadata',
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
        commands.append(('system - available commands', '??'))
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
        if (path.startswith(score_storehouses) and
            not getattr(self, '_simple_score_annotation', False)):
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
        elif (path.startswith(score_storehouses) and
            getattr(self, '_simple_score_annotation', False)):
            if self._configuration.example_score_packages_directory in path:
                annotation = 'Example scores'
            else:
                annotation = 'Scores'
        elif path.startswith(
            self._configuration.library_makers_directory):
            last_name = self._configuration.composer_last_name
            annotation = '{} maker library'.format(last_name)
        elif path.startswith(
            self._configuration.library_material_packages_directory):
            last_name = self._configuration.composer_last_name
            annotation = '{} material library'.format(last_name)
        elif path.startswith(
            self._configuration.library_stylesheets_directory):
            last_name = self._configuration.composer_last_name
            annotation = '{} stylesheet library'.format(last_name)
        elif path.startswith(self._configuration.abjad_stylesheets_directory):
            annotation = 'Abjad stylesheets'
        elif path.startswith(
            self._configuration.example_material_packages_directory):
            annotation = 'Example material packages'
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
        return string

    def _path_to_human_readable_name(self, path):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        include_extensions = self._include_extensions
        if not include_extensions:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    def _read_view(self):
        view_name = self._read_view_name()
        if not view_name:
            return
        view_inventory = self._read_view_inventory()
        if not view_inventory:
            return
        return view_inventory.get(view_name)

    def _read_view_inventory(self):
        from scoremanager import idetools
        if self._views_py_path is None:
            return
        if not os.path.exists(self._views_py_path):
            return
        result = self._io_manager.execute_file(
            path=self._views_py_path,
            attribute_names=('view_inventory',),
            )
        if result == 'corrupt':
            messages = []
            message = '{} __views.py__ is corrupt:'
            message = message.format(type(self).__name__)
            messages.append(message)
            messages.append('')
            message = '    {}'.format(self._views_py_path)
            messages.append(message)
            self._io_manager._display(messages)
            return
        if not result:
            return
        assert len(result) == 1
        view_inventory = result[0]
        if view_inventory is None:
            view_inventory = idetools.ViewInventory()
        items = list(view_inventory.items())
        view_inventory = idetools.ViewInventory(items)
        return view_inventory

    def _read_view_name(self):
        if self._session.is_test:
            return
        if self._session.is_in_score:
            manager = self._current_package_manager
            metadatum_name = 'view_name'
        else:
            manager = self._views_package_manager
            metadatum_name = '{}_view_name'.format(type(self).__name__)
        if not manager:
            return
        return manager._get_metadatum(metadatum_name)

    def _remove_unadded_assets(self, dry_run=False):
        paths = self._get_unadded_asset_paths()
        inputs, outputs = [], []
        if dry_run:
            inputs, outputs = paths, []
            return inputs, outputs
        elif not paths:
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
            show = self._session.display_available_commands
            self._session._display_available_commands = not show

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

    def go_to_all_build_files(self):
        r'''Goes to all build files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_build_files = True

    def go_to_all_distribution_files(self):
        r'''Goes to all distribution files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_distribution_files = True

    def go_to_all_maker_files(self):
        r'''Goes to all maker files.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_maker_files = True

    def go_to_all_materials(self):
        r'''Goes to all materials.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_materials = True

    def go_to_all_segments(self):
        r'''Goes to all segments.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_segments = True

    def go_to_all_stylesheets(self):
        r'''Goes to all stylesheets.

        Returns none.
        '''
        self.go_to_all_scores()
        self._session._is_navigating_to_stylesheets = True

    def invoke_python(self):
        r'''Invokes Python.

        Returns none.
        '''
        messages = []
        prompt = True
        statement = self._io_manager._handle_input(
            '>>', 
            include_newline=False,
            )
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

    def invoke_shell(self):
        r'''Invokes shell.

        Returns none.
        '''
        statement = self._io_manager._handle_input(
            '$',
            include_chevron=False,
            include_newline=False,
            )
        statement = statement.strip()
        self._io_manager._invoke_shell(statement)

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

    def write_metadata_py(self, dry_run=False):
        r'''Writes ``__metadata.py__``.

        Returns none.
        '''
        inputs, outputs = [], []
        inputs.append(self._metadata_py_path)
        if dry_run:
            return inputs, outputs
        messages = self._format_messaging(inputs, outputs, verb='write')
        self._io_manager._display(messages)
        # WEIRD: why can't this confirm check be removed?
        if self._session.confirm:
            result = self._io_manager._confirm()
            if self._session.is_backtracking or not result:
                return
        metadata = self._get_metadata()
        self._write_metadata_py(metadata)