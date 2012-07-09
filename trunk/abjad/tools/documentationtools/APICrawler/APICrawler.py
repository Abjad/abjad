import os
import types
from abjad.tools import abctools
from abjad.tools.documentationtools.ClassDocumenter import ClassDocumenter
from abjad.tools.documentationtools.FunctionDocumenter import FunctionDocumenter
from abjad.tools.documentationtools.ModuleCrawler import ModuleCrawler


class APICrawler(abctools.AbjadObject):
    '''Generates directories containing ReST to parallel directories containing code.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_code_root', '_docs_root', '_module_crawler', '_prefix')

    ### INITIALIZER ###

    def __init__(self, code_root, docs_root, root_package_name,
        ignored_directories = ['test', '.svn', '__pycache__'],
        prefix='abjad.tools.'):
        self._module_crawler = ModuleCrawler(code_root,
            root_package_name=root_package_name,
            ignored_directories=ignored_directories)
        assert os.path.exists(docs_root)
        self._code_root = os.path.abspath(code_root)
        self._docs_root = os.path.abspath(docs_root)
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Crawl `code_root` and generate corresponding ReST in `docs_root` 
        while ignoring ignored directories.
        '''
        assert os.path.exists(self.docs_root)

        documenters = []

        for module in self.module_crawler:
            obj_name = module.__name__.split('.')[-1]
            if not hasattr(module, obj_name) or obj_name.startswith('_'):
                continue

            # get object and documenter
            obj = getattr(module, obj_name)
            if isinstance(obj, types.TypeType):
                documenter = ClassDocumenter(obj, prefix=self.prefix)
            elif isinstance(obj, types.FunctionType):
                documenter = FunctionDocumenter(obj, prefix=self.prefix)

            # create directory
            code_directory = os.path.dirname(module.__file__)
            docs_directory = code_directory.replace(self.code_root, self.docs_root)
            if not os.path.exists(docs_directory):
                print 'CREATING DIRECTORY: {}'.format(os.path.relpath(docs_directory))
                os.makedirs(docs_directory)

            # create ReST, if changed
            docs_file = '{}.rst'.format(module.__file__.rpartition('.py')[0].replace(self.code_root, self.docs_root))
            new_docs = documenter()
            if os.path.exists(docs_file):
                file_handler = open(docs_file, 'r')
                old_docs = file_handler.read()
                file_handler.close()
            else:
                old_docs = None

            # only overwrite if changed
            if new_docs != old_docs:
                if old_docs is not None:
                    print 'UPDATING {}'.format(os.path.relpath(docs_file))
                else:
                    print 'CREATING {}'.format(os.path.relpath(docs_file))
                file_handler = open(docs_file, 'w')
                file_handler.write(new_docs)
                file_handler.close()

            documenters.append(documenter)

        return tuple(sorted(documenters, key=lambda x: x.module_name))

    ### PUBLIC PROPERTIES ###

    @property
    def code_root(self):
        return self._code_root

    @property
    def docs_root(self):
        return self._docs_root

    @property
    def module_crawler(self):
        return self._module_crawler

    @property
    def prefix(self):
        return self._prefix
