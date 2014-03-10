# -*- encoding: utf-8 -*-
import os
from abjad.tools.abctools import AbjadObject


class ModuleCrawler(AbjadObject):
    r'''Crawls `code_root`, yielding all module objects whose name begins with
    `root_package_name`.

    Return `ModuleCrawler` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_code_root',
        '_ignored_directory_names',
        '_root_package_name',
        '_visit_private_modules',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        code_root=None,
        ignored_directory_names=(
            '__pycache__',
            '.git',
            '.svn',
            'test',
            ),
        root_package_name=None,
        visit_private_modules=False,
        ):
        from abjad import abjad_configuration
        if code_root is None:
            code_root = abjad_configuration.abjad_directory_path
        assert os.path.exists(code_root)
        if not os.path.exists(os.path.join(code_root, '__init__.py')):
            message = '{} is not a Python package directory.'
            message = message.format(code_root)
            raise ValueError(message)
        code_root = os.path.abspath(code_root)

        if root_package_name is None:
            parts = code_root.split(os.path.sep)
            root_package_name = parts[-1]
            while os.path.exists(os.path.join(
                os.path.sep.join(parts), '__init__.py')):
                root_package_name = parts.pop()

        self._code_root = code_root
        self._ignored_directory_names = ignored_directory_names
        self._root_package_name = root_package_name
        self._visit_private_modules = bool(visit_private_modules)

    ### SPECIAL METHODS ###

    def __iter__(self, include_score_manager=False):
        r'''Iterates module crawler.

        Returns generator.
        '''
        assert os.path.exists(self.code_root)

        if not os.path.exists(os.path.join(self.code_root, '__init__.py')):
            return

        for current_root, directories, files in os.walk(self.code_root):

            # filter directories
            for directory in directories[:]:
                if directory in self.ignored_directory_names:
                    directories.remove(directory)
                elif directory.startswith('_') and \
                    not self.visit_private_modules:
                    directories.remove(directory)
                elif not os.path.exists(os.path.join(
                    current_root, directory, '__init__.py')):
                    directories.remove(directory)
            directories.sort()

            # filter files
            for file in files[:]:
                if file.startswith('__'):
                    files.remove(file)
                elif not file.endswith('.py'):
                    files.remove(file)
            files.sort()

            # process files
            for file in files:
                path = os.path.join(current_root, file).replace('.py', '')
                parts = path.split(os.path.sep)
                object_name = parts[-1]
                module_name = []
                for part in reversed(parts):
                    module_name.append(part)
                    if part == self.root_package_name:
                        break
                module_name = '.'.join(reversed(module_name))
                module = __import__(module_name, fromlist=['*'])
                yield module

    ### PUBLIC PROPERTIES ###

    @property
    def code_root(self):
        r'''Code root of module crawler.

        Returns string.
        '''
        return self._code_root

    @property
    def ignored_directory_names(self):
        r'''Ignored directory names of module crawler.

        Returns tuple.
        '''
        return self._ignored_directory_names

    @property
    def root_package_name(self):
        r'''Root package name of module crawler.

        Returns string.
        '''
        return self._root_package_name

    @property
    def visit_private_modules(self):
        r'''Visit private modules.

        Returns boolean.
        '''
        return self._visit_private_modules
