import os
from abjad.tools.abctools import AbjadObject


class ModuleCrawler(AbjadObject):
    '''Crawls `code_root`, yielding all module objects whose name begins with
    `root_package_name`.

    Return `ModuleCrawler` instance.
    '''
    
    ### CLASS ATTRIBUTES ###
    
    __slots__ = ('_code_root', '_ignored_directories', '_root_package_name')

    ### INITIALIZER ###

    def __init__(self, code_root,
        ignored_directories=['test', '.svn', '__pycache__'],
        root_package_name='abjad'):
        assert os.path.exists(code_root)
        assert root_package_name in code_root.split(os.path.sep)
        self._code_root = os.path.abspath(code_root)
        self._ignored_directories = ignored_directories
        self._root_package_name = root_package_name

    ### SPECIAL METHODS ###

    def __iter__(self):
        assert os.path.exists(self.code_root)
        for current_root, directories, files in os.walk(self.code_root):

            # filter directories
            for directory in directories[:]:
                if directory in self.ignored_directories:
                    directories.remove(directory)
                elif directory.startswith('_'):
                    directories.remove(directory)
                elif not os.path.exists(os.path.join(current_root, directory, '__init__.py')):
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
                module_name = [ ]
                for part in reversed(parts):
                    module_name.append(part)
                    if part == self.root_package_name:
                        break
                module_name = '.'.join(reversed(module_name))
                module = __import__(module_name, fromlist=['*'])
                yield module

    ### PUBLIC ATTRIBUTES ###

    @property
    def code_root(self):
        return self._code_root

    @property
    def ignored_directories(self):
        return self._ignored_directories

    @property
    def root_package_name(self):
        return self._root_package_name
