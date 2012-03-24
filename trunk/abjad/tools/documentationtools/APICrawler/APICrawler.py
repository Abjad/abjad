import os
import types
from abjad.tools import abctools
from abjad.tools.documentationtools.ClassDocumenter import ClassDocumenter
from abjad.tools.documentationtools.FunctionDocumenter import FunctionDocumenter


class APICrawler(abctools.AbjadObject):
    '''Generates directories containing ReST to parallel directories containing code.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_code_root', '_docs_root', '_ignored_directories', '_prefix', '_root_package_name')

    ### INITIALIZER ###

    def __init__(self, code_root, docs_root, root_package_name,
        ignored_directories = ['test', '.svn', '__pycache__'],
        prefix='abjad.tools.'):
        assert os.path.exists(code_root)
        assert os.path.exists(docs_root)
        assert root_package_name in code_root.split(os.path.sep)
        self._code_root = os.path.abspath(code_root)
        self._docs_root = os.path.abspath(docs_root)
        self._ignored_directories = ignored_directories
        self._root_package_name = root_package_name
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Crawl `code_root` and generate corresponding ReST in `docs_root` 
        while ignoring ignored directories.
        '''
        assert os.path.exists(self.code_root)
        assert os.path.exists(self.docs_root)

        visited_modules = [ ]
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
                if file.startswith('_'):
                    files.remove(file)
                elif not file.endswith('.py'):
                    files.remove(file)
            files.sort()

            # process directories
            for directory in directories:
                docs_directory = os.path.join(current_root, directory).replace(self.code_root, self.docs_root)
                if not os.path.exists(docs_directory):
                    print 'CREATING DIRECTORY: %s' % docs_directory
                    os.mkdir(docs_directory)

            # process files
            for file in files:

                # get documenter
                print current_root, file
                obj = self._get_documenter_for_file(current_root, file)
                code_fullpath = os.path.join(current_root, file)
                docs_fullpath = code_fullpath.replace(self.code_root, self.docs_root).replace('.py', '.rst')
                new_docs = obj()

                # read old docs
                if os.path.exists(docs_fullpath):
                    file_handler = open(docs_fullpath, 'r')
                    old_docs = file_handler.read()
                    file_handler.close()
                else:
                    old_docs = None

                # only overwrite if changed
                if new_docs != old_docs:
                    file_handler = open(docs_fullpath, 'w')
                    file_handler.write(new_docs)
                    file_handler.close()

                # add module of documenter's documentary subject to visited modules list
                visited_modules.append(obj)

        return tuple(sorted(visited_modules, key=lambda x: x.module_name))

    ### PRIVATE METHODS ###

    def _get_documenter_for_file(self, current_root, file):
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
        obj = getattr(module, object_name)

        if isinstance(obj, types.TypeType):
            return ClassDocumenter(obj, prefix=self.prefix)
        elif isinstance(obj, types.FunctionType):
            return FunctionDocumenter(obj, prefix=self.prefix)
        raise Exception("Don't know how to document %r." % obj)

    ### PUBLIC ATTRIBUTES ###

    @property
    def code_root(self):
        return self._code_root

    @property
    def docs_root(self):
        return self._docs_root

    @property
    def ignored_directories(self):
        return self._ignored_directories

    @property
    def prefix(self):
        return self._prefix

    @property
    def root_package_name(self):
        return self._root_package_name
