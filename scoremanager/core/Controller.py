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
    def _input_to_method(self):
        result = {
            'b': self.go_back,
            'h': self.go_home,
            's': self.go_to_current_score,
            }
        return result

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_directory_with_metadata_py(path):
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

    def _list_directories_with_metadata_pys(self, path=None):
        path = path or self._path
        paths = []
        for directory_path, subdirectory_names, file_names in os.walk(path):
            if self._is_directory_with_metadata_py(directory_path):
                if directory_path not in paths:
                    paths.append(directory_path)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory_path, subdirectory_name)
                if self._is_directory_with_metadata_py(path):
                    if path not in paths:
                        paths.append(path)
        return paths

    def _list_python_files_in_visible_assets(self):
        assets = []
        paths = self._list_visible_asset_paths()
        for path in paths:
            if os.path.isdir(path):
                triples = os.walk(path)
                for directory_path, subdirectory_names, file_names in triples:
                    for file_name in file_names:
                        if file_name.endswith('.py'):
                            file_path = os.path.join(
                                directory_path, 
                                file_name,
                                )
                            assets.append(file_path)
            elif os.path.isfile(path) and path.endswith('.py'):
                assets.append(path)
        return assets

    def _make_done_menu_section(self, menu):
        commands = []
        commands.append(('done', 'done'))
        menu.make_navigation_section(
            commands=commands,
            name='zzz - done',
            )

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
        commands.append(('__metadata__.py - open', 'mdpyo'))
        commands.append(('__metadata__.py - rewrite', 'mdpyrw'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='__metadata__.py',
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

    @staticmethod
    def _remove_file_line(file_path, line_to_remove):
        lines_to_keep = []
        with open(file_path, 'r') as file_pointer:
            for line in file_pointer.readlines():
                if line == line_to_remove:
                    pass
                else:
                    lines_to_keep.append(line)
        with open(file_path, 'w') as file_pointer:
            contents = ''.join(lines_to_keep)
            file_pointer.write(contents)

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

    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._hide_hidden_commands = True

    def go_home(self):
        r'''Goes home.

        Returns none.
        '''
        self._session._is_backtracking_to_score_manager = True
        self._session._hide_hidden_commands = True

    def go_to_current_score(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._hide_hidden_commands = True