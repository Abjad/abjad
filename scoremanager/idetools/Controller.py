# -*- encoding: utf -*-
import abc
import os
from abjad.tools import stringtools


class Controller(object):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    __slots__ = (
        '_configuration',
        '_controller_context',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INTIIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import idetools
        self._configuration = idetools.Configuration()
        self._session = session or idetools.Session()
        self._io_manager = idetools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript
        # TODO: maybe remove this property?
        self._controller_context = idetools.ControllerContext(controller=self)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    def __hash__(self):
        r'''Hashes controller.
        '''
        return hash((type(self), self._session))

    def __ne__(self, expr):
        r'''Is true when types are not the same. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of controller.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    @property
    def _breadcrumb(self):
        pass

    @property
    def _input_to_method(self):
        result = {
            '**': self.go_to_library,
            'b': self.go_back,
            'h': self.go_home,
            'q': self.quit,
            's': self.go_to_current_score,
            }
        return result

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_directory_with_metadata_py(path):
        if os.path.isdir(path):
            for directory_entry in os.listdir(path):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    def _list_directories_with_metadata_pys(self, path=None):
        path = path or self._path
        paths = []
        for directory, subdirectory_names, file_names in os.walk(path):
            if self._is_directory_with_metadata_py(directory):
                if directory not in paths:
                    paths.append(directory)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory, subdirectory_name)
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
                for directory, subdirectory_names, file_names in triples:
                    for file_name in file_names:
                        if file_name.endswith('.py'):
                            file_path = os.path.join(
                                directory, 
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
        with open(file_path, 'r') as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                line = line.replace(old, new)
                new_file_lines.append(line)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(''.join(new_file_lines))

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary
        
    @staticmethod
    def _trim_path(path, width=80):
        if width and width < len(path):
            path = '...' + path[-width:]
        return path

    ### PUBLIC METHODS ###

    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        self._session._is_backtracking_locally = True
        self._session._display_available_commands = False

    def go_home(self):
        r'''Goes home.

        Returns none.
        '''
        self._session._is_backtracking_to_score_manager = True
        self._session._display_available_commands = False

    def go_to_current_score(self):
        r'''Goes to current score.

        Returns none.
        '''
        if self._session.is_in_score:
            self._session._is_backtracking_to_score = True
            self._session._display_available_commands = False

    def go_to_library(self):
        r'''Goes to library.

        Returns none.
        '''
        self._session._is_backtracking_to_library = True
        self._session._display_available_commands = False

    def quit(self):
        r'''Quits.

        Returns none.
        '''
        self._session._is_quitting = True
        self._session._display_available_commands = False