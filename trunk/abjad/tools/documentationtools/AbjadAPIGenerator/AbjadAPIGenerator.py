import importlib
import os
from abjad.tools import abctools
from abjad.tools.documentationtools.APICrawler import APICrawler
from abjad.tools.documentationtools.ClassDocumenter import ClassDocumenter
from abjad.tools.documentationtools.FunctionDocumenter import FunctionDocumenter


class AbjadAPIGenerator(abctools.AbjadObject):
    '''Creates Abjad's API ReST:

        * writes ReST pages for individual classes and functions
        * writes the API index ReST
        * handles sorting tools packages into composition, manual-loading and unstable
        * handles ignoring private tools packages

    Returns `AbjadAPIGenerator` instance.
    '''

    ### CLASS ATTRIBUTES ###

    _api_title = 'Abjad API'

    _package_descriptions = {
        'core': 'Core composition packages',
        'demos': 'Demos and example packages',
        'internals': 'Abjad internal packages',
        'unstable': 'Unstable packages (load manually)',
    }

    _undocumented_packages = (
        'lilypondproxytools',
    )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, verbose=False):

        if verbose:
            print 'Now making Sphinx TOCs ...'

        ignored_directories = ['.svn', 'test', '__pycache__']
        ignored_directories.extend(self._undocumented_packages)

        all_visited_modules = []
        for code_path, docs_path, package_prefix in self.path_definitions:
            if not os.path.exists(code_path):
                os.makedirs(code_path)
            if not os.path.exists(docs_path):
                os.makedirs(docs_path)
            crawler = APICrawler(code_path, docs_path, self.root_package,
                ignored_directories=ignored_directories, prefix=package_prefix)
            all_visited_modules.extend(crawler())
        package_dictionary = self._sort_modules(all_visited_modules)

        if verbose:
            print 'Now making API index ...'

        result = []

        result.extend(self._create_heading(self._api_title))

        for package_group, packages in sorted(package_dictionary.items()):
            if packages:
                result.extend(self._create_section_title(
                    self._package_descriptions[package_group]))
                for package_name, package in sorted(packages.items()):
                    result.extend(self._create_package_toc(package_name, package))

        f = open(self.docs_api_index_path, 'w')
        f.write('\n'.join(result))
        f.close()

        if verbose:
            print ''
            print '... Done.'
            print ''

    ### PRIVATE METHODS ###

    def _create_heading(self, text, character='='):
        return [text, character * len(text), '']

    def _create_package_title(self, package_name):
        result = self._create_heading(':py:mod:`%s <%s%s>`' % 
            (package_name, self.package_prefix, package_name), '~')
        return result

    def _create_package_toc(self, package_name, package_modules):
        result = []
        result.extend(self._create_package_title(package_name))

        if package_modules['abstract_classes']:
            result.extend(self._create_toc_directive())
            for obj in package_modules['abstract_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')
        
        if package_modules['concrete_classes']:
            if package_modules['abstract_classes']:
                result.append('\n--------\n')
            result.extend(self._create_toc_directive())
            for obj in package_modules['concrete_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')

        if package_modules['functions']:
            if package_modules['concrete_classes'] or package_modules['abstract_classes']:
                result.append('\n--------\n')
            result.extend(self._create_toc_directive())
            for obj in package_modules['functions']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')

        return result

    def _create_section_title(self, title):
        result = self._create_heading(title, '-')
        result.extend(self._create_toc_directive())
        return result

    def _create_toc_directive(self):
        return [
            '.. toctree::',
            '   :maxdepth: 1',
            ''
        ]

    def _module_name_to_toc_entry(self, module_name):
        parts = module_name.split('.')[self.tools_package_path_index-1:-1]
        return '   %s' % '/'.join(parts)

    def _sort_modules(self, objects):

        packages = {}

        for obj in sorted(objects, key=lambda x: x.module_name):

            tools_package_name = obj.module_name.split('.')[self.tools_package_path_index]
            tools_package_path = '.'.join(obj.module_name.split('.')[:self.tools_package_path_index + 1])
            tools_package_module = importlib.import_module(tools_package_path)

            if hasattr(tools_package_module, '_documentation_section'):
                declared_documentation_section = getattr(tools_package_module, '_documentation_section')
                if declared_documentation_section not in packages:
                    packages[declared_documentation_section] = {}
                collection = packages[declared_documentation_section]
            else:
                continue

            if tools_package_name not in collection:
                collection[tools_package_name] = {
                    'abstract_classes': [],
                    'concrete_classes': [],
                    'functions': []
                }

            if isinstance(obj, ClassDocumenter):
                if obj.is_abstract:
                    collection[tools_package_name]['abstract_classes'].append(obj)
                else:
                    collection[tools_package_name]['concrete_classes'].append(obj)
            else:
                collection[tools_package_name]['functions'].append(obj)

        return packages
        

    ### PUBLIC PROPERTIES ###

    @property
    def docs_api_index_path(self):
        '''Path to index.rst for Abjad API.'''
        from abjad import ABJCFG
        return os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'index.rst')

    @property
    def package_prefix(self):
        return ('abjad.tools.', 'abjad.demos.')

    @property
    def path_definitions(self):
        '''Code path / docs path / package prefix triples.'''
        from abjad import ABJCFG
        return (
            (
                os.path.join(ABJCFG.ABJAD_PATH, 'tools'),
                os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'tools'),
                'abjad.tools.',
            ),
            (
                os.path.join(ABJCFG.ABJAD_PATH, 'demos'),
                os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'demos'),
                'abjad.demos.',
            ),
        )

    @property
    def root_package(self):
        return 'abjad'

    @property
    def tools_package_path_index(self):
        return 2
