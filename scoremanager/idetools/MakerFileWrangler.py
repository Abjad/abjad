# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools
from abjad.tools import stringtools
from scoremanager.idetools.FileWrangler import FileWrangler


class MakerFileWrangler(FileWrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.idetools.Session()
            >>> wrangler = scoremanager.idetools.MakerFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'maker'
        self._basic_breadcrumb = 'makers'
        self._extension = '.py'
        self._force_lowercase = False
        self._in_library = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.makers_library

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(MakerFileWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'ne': self.edit_init_py,
            'nl': self.list_init_py,
            'ns': self.write_stub_init_py,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_maker_files = False

    @staticmethod
    def _file_name_callback(file_name):
        base_name, extension = os.path.splitext(file_name)
        base_name = stringtools.to_upper_camel_case(base_name)
        file_name = base_name + extension
        return file_name

    def _is_valid_directory_entry(self, directory_entry):
        name, extension = os.path.splitext(directory_entry)
        if stringtools.is_upper_camel_case(name):
            if extension == '.py':
                return True
        return False

    def _list_maker_classes(self):
        modules = self._list_maker_modules()
        classes = documentationtools.list_all_classes(
            modules=modules)
        return classes

    def _list_maker_modules(self):
        paths = self._list_storehouse_paths()
        packages = []
        for path in paths:
            package = self._configuration.path_to_package(path)
            packages.append(package)
        modules = []
        for package in packages:
            statement = 'import {} as _module'.format(package)
            try:
                result = self._io_manager.execute_string(
                    statement,
                    ('_module',),
                    )
                _module = result[0]
                modules.append(_module)
            except ImportError:
                pass
        return modules

    def _make_main_menu(self):
        superclass = super(MakerFileWrangler, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    def edit_init_py(self):
        r'''Edits ``__init__.py``.

        Returns none.
        '''
        self._open_file(self._init_py_file_path)

    def list_init_py(self):
        r'''Lists ``__init__.py``.

        Returns none.
        '''
        self._io_manager._display(self._init_py_file_path)

    def write_stub_init_py(self):
        r'''Writes stub ``__init__.py``.

        Returns none.
        '''
        path = self._init_py_file_path
        message = 'will write stub to {}.'
        message = message.format(path)
        self._io_manager._display(message)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        self._io_manager.write_stub(self._init_py_file_path)