# -*- encoding: utf -*-
import os
import re
from abjad.tools import developerscripttools
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Controller(ScoreManagerObject):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        superclass = super(Controller, self)
        superclass.__init__(session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    @property
    def _user_input_to_action(self):
        result = {
            }
        return result

    ### PRIVATE METHODS ###

    def _filter_asset_menu_entries_by_view(self, entries, view):
        entries = entries[:]
        filtered_entries = []
        for item in view:
            try:
                pattern = re.compile(item)
            except:
                pattern = None
                message = 'invalid regular expression: {!r}.'
                message  = message.format(item)
                self._io_manager.proceed(message)
            for entry in entries:
                display_string, _, _, path = entry
                if self._session.is_in_score:
                    string = self._get_without_annotation(display_string)
                else:
                    string = display_string
                if item == string:
                    filtered_entries.append(entry)
                elif pattern and pattern.match(string):
                    filtered_entries.append(entry)
        return filtered_entries

    @staticmethod
    def _get_without_annotation(display_string):
        if not display_string.endswith(')'):
            return display_string
        index = display_string.find('(')
        result = display_string[:index]
        result = result.strip()
        return result

    @staticmethod
    def _is_directory_with_metadata_module(path):
        if os.path.isdir(path):
            for directory_entry in os.listdir(path):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    @staticmethod
    def _is_package_path(path):
        if os.path.isdir(path):
            for directory_entry in os.listdir(path):
                if directory_entry == '__init__.py':
                    return True
        return False

    def _list_directories_with_metadata_modules(self, path=None):
        path = path or self._path
        paths = []
        for directory_path, subdirectory_names, file_names in os.walk(path):
            if self._is_directory_with_metadata_module(directory_path):
                if directory_path not in paths:
                    paths.append(directory_path)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory_path, subdirectory_name)
                if self._is_directory_with_metadata_module(path):
                    if path not in paths:
                        paths.append(path)
        return paths

    def _list_python_files_in_visible_assets(self, tests_only=False):
        assets = []
        if self._session.is_in_score:
            current_directory = self._get_current_directory_path()
            paths = [current_directory]
        else:
            paths = self._list_visible_asset_paths()
        for path in paths:
            if os.path.isdir(path):
                triples = os.walk(path)
                for directory_path, subdirectory_names, file_names in triples:
                    for file_name in file_names:
                        if file_name.endswith('.py'):
                            if not tests_only or file_name.startswith('test_'):
                                file_path = os.path.join(
                                    directory_path, 
                                    file_name,
                                    )
                                assets.append(file_path)
            elif os.path.isfile(path) and path.endswith('.py'):
                assets.append(path)
        return assets

    def _make_asset_menu_entries(
        self,
        apply_view=True,
        include_annotation=True,
        include_extensions=False,
        include_asset_name=True,
        include_year=False,
        human_readable=True,
        packages_instead_of_paths=False,
        sort_by_annotation=True,
        ):
        paths = self._list_visible_asset_paths()
        strings = []
        for path in paths:
            if human_readable:
                string = self._path_to_human_readable_name(
                    path,
                    include_extension=include_extensions,
                    )
            else:
                string = os.path.basename(path)
            if include_annotation:
                annotation = self._path_to_annotation(path, year=include_year)
                if include_asset_name:
                    string = '{} ({})'.format(string, annotation)
                else:
                    string = str(annotation)
            strings.append(string)
        pairs = zip(strings, paths)
        if sort_by_annotation:
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
        entries = []
        for string, path in pairs:
            if packages_instead_of_paths:
                path = self._configuration.path_to_package_path(path)
            entry = (string, None, None, path)
            entries.append(entry)
        if self._session.is_test:
            return entries
        if not apply_view:
            return entries
        view = self._read_view()
        if view is not None:
            entries = self._filter_asset_menu_entries_by_view(entries, view)
        return entries

    def _make_directory_menu_section(self, menu, is_permanent=False):
        commands = []
        commands.append(('directory - list', 'ls'))
        commands.append(('directory - list long', 'll'))
        if not is_permanent:
            commands.append(('directory - remove', 'rm'))
            commands.append(('directory - rename', 'ren'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='directory',
            )

    def _make_done_menu_section(self, menu):
        commands = []
        commands.append(('done', 'done'))
        menu.make_navigation_section(
            commands=commands,
            name='zzz - done',
            )

    def _make_initializer_menu_section(self, menu):
        commands = []
        if (self._initializer_file_path and
            os.path.isfile(self._initializer_file_path)):
            commands.append(('initializer - remove', 'inrm'))
            commands.append(('initializer - read only', 'inro'))
        else:
            commands.append(('initializer - stub', 'ins'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='initializer',
            )

    def _make_metadata_menu_section(self, menu):
        commands = []
        commands.append(('metadatum - add', 'mda'))
        commands.append(('metadatum - get', 'mdg'))
        commands.append(('metadatum - remove', 'mdrm'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadatum',
            )

    def _make_metadata_module_menu_section(self, menu):
        commands = []
        commands.append(('metadata module - remove', 'mdmrm'))
        commands.append(('metadata module - rewrite', 'mdmrw'))
        commands.append(('metadata module - read only', 'mdmro'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadata module',
            )

    def _make_sibling_asset_tour_menu_section(self, menu):
        section = menu['go - scores']
        menu.menu_sections.remove(section)
        commands = []
        commands.append(('go - next score', '>>'))
        commands.append(('go - previous score', '<<'))
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

    def _make_views_menu_section(self, menu):
        commands = []
        commands.append(('views - apply', 'va'))
        commands.append(('views - list', 'vls'))
        commands.append(('views - new', 'vnew'))
        commands.append(('views - remove', 'vrm'))
        commands.append(('views - rename', 'vren'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views',
            )

    def _make_views_module_menu_section(self, menu):
        commands = []
        commands.append(('views module - remove', 'vmrm'))
        commands.append(('views module - read only', 'vmro'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views module',
            )

    def _path_to_annotation(self, path, year=False):
        from scoremanager import managers
        score_storehouses = (
            self._configuration.example_score_packages_directory_path,
            self._configuration.user_score_packages_directory_path,
            )
        if path.startswith(score_storehouses):
            score_path = self._configuration._path_to_score_path(path)
            manager = managers.ScorePackageManager(
                path=score_path,
                session=self._session,
                )
            metadata = manager._get_metadata()
            if metadata:
                year_of_completion = metadata.get('year_of_completion')
                title = metadata.get('title')
                if year and year_of_completion:
                    annotation = '{} ({})'.format(title, year_of_completion)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = 'Untitled ({})'
                annotation = annotation.format(package_name)
        elif path.startswith(self._user_storehouse_path):
            annotation = self._configuration.composer_last_name
        elif path.startswith(self._abjad_storehouse_path):
            annotation = 'Abjad'
        else:
            annotation = None
        return annotation

    @staticmethod
    def _path_to_human_readable_name(path, include_extension=False):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        if not include_extension:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    @staticmethod
    def _replace_in_file(file_path, old, new):
        with file(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(new_file_lines))

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary

    ### PUBLIC METHODS ###

    def doctest(self):
        r'''Runs doctest on Python files contained in visible assets.

        Returns none.
        '''
        from scoremanager import managers
        assets = []
        if isinstance(self, managers.Manager):
            paths = [self._path]
        else:
            paths = self._list_visible_asset_paths()
        for path in paths:
            if path.endswith('.py'):
                assets.append(path)
            if os.path.isdir(path):
                triples = os.walk(path)
                for directory_name, subdirectories, file_names in triples:
                    for file_name in file_names:
                        if file_name.endswith('.py'):
                            file_path = os.path.join(directory_name, file_name)
                            assets.append(file_path)
        if not assets:
            message = 'no testable assets found.'
            self._io_manager.display([message, ''])
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
            if strings:
                strings.append('')
            self._io_manager.display(strings, capitalize=False)
        self._session._hide_next_redraw = True

    def pytest(self):
        r'''Runs py.test on Python files contained in visible assets.

        Returns none.
        '''
        assets = []
        paths = self._list_python_files_in_visible_assets(tests_only=True)
        for path in paths:
            if os.path.isdir(path):
                assets.append(path)
            elif os.path.isfile(path) and path.endswith('.py'):
                assets.append(path)
        if not assets:
            message = 'no testable assets found.'
            self._io_manager.display([message, ''])
        else:
            count = len(paths)
            identifier = stringtools.pluralize('asset', count=count)
            message = '{} testable {} found ...'
            message = message.format(count, identifier)
            self._io_manager.display([message, ''])
            assets = ' '.join(assets)
            command = 'py.test -rf {}'.format(assets)
            self._io_manager.run_command(command, capitalize=False)
        self._session._hide_next_redraw = True