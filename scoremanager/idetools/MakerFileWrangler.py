# -*- encoding: utf-8 -*-
import os
import traceback
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
        from scoremanager import idetools
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'maker files'
        self._extension = '.py'
        self._force_lowercase = False
        self._in_user_library = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_maker_files = False

    def _is_valid_directory_entry(self, directory_entry):
        name, extension = os.path.splitext(directory_entry)
        if stringtools.is_upper_camel_case(name):
            if extension == '.py':
                return True
        return False

    def _list_maker_classes(self):
        modules = self._list_maker_modules()
        classes = documentationtools.list_all_experimental_classes(
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
                exec(statement)
                modules.append(_module)
            except ImportError:
                pass
        return modules