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

    _composition_packages_description = 'Composition packages'

    _internals_packages_description = 'Internal packages'

    _manual_packages_description = 'Additional packages (load manually)'

    _undocumented_packages = (
        'lilypondproxytools',
    )

    _unstable_packages_description = 'Unstable packages (load manually)'

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, verbose=False):
        assert os.path.exists(self.code_tools_path)
        assert os.path.exists(self.docs_tools_path)

        if verbose:
            print 'Now making Sphinx TOCs ...'

        ignored_directories = ['.svn', 'test', '__pycache__']
        ignored_directories.extend(self._undocumented_packages)
        tools_crawler = APICrawler(self.code_tools_path, self.docs_tools_path, self.root_package,
            ignored_directories = ignored_directories, prefix=self.package_prefix)
        visited_modules = tools_crawler()

        composition, manual, unstable, internals = self._sort_modules(visited_modules)

        if verbose:
            print 'Now making API index ...'

        result = []

        result.extend(self._create_heading(self._api_title))

        # automatically loading composition packages
        if composition:
            result.extend(self._create_section_title(self._composition_packages_description))
            for package_name in sorted(composition):
                result.extend(self._create_package_toc(package_name, composition[package_name]))

        # manually loading composition packages
        if manual:
            result.extend(self._create_section_title(self._manual_packages_description))
            for package_name in sorted(manual):
                result.extend(self._create_package_toc(package_name, manual[package_name]))

        # unstable composition packages
        if unstable:
            result.extend(self._create_section_title(self._unstable_packages_description))
            for package_name in sorted(unstable):
                result.extend(self._create_package_toc(package_name, unstable[package_name]))

        # internals packages
        if internals:
            result.extend(self._create_section_title(self._internals_packages_description))
            for package_name in sorted(internals):
                result.extend(self._create_package_toc(package_name, internals[package_name]))

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
            result.append('.. rubric:: abstract classes\n')
            result.extend(self._create_toc_directive())
            for obj in package_modules['abstract_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')
        if package_modules['concrete_classes']:
            result.append('.. rubric:: concrete classes\n')
            result.extend(self._create_toc_directive())
            for obj in package_modules['concrete_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')
        if package_modules['functions']:
            result.append('.. rubric:: functions\n')
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
        composition = {}
        internals = {}
        manual = {}
        unstable = {}

        for obj in sorted(objects, key=lambda x: x.module_name):

            tools_package_name = obj.module_name.split('.')[self.tools_package_path_index]
            tools_package_path = '.'.join(obj.module_name.split('.')[:self.tools_package_path_index + 1])
            tools_package_module = importlib.import_module(tools_package_path)

            collection = manual
            if hasattr(tools_package_module, '_documentation_section'):
                declared_documentation_section = getattr(tools_package_module, '_documentation_section')
                if declared_documentation_section == 'core':
                    collection = composition
                elif declared_documentation_section == 'internals':
                    collection = internals
                elif declared_documentation_section == 'manual':
                    collection = manual
                elif declared_documentation_section == 'undocumented':
                    continue
                elif declared_documentation_section == 'unstable':
                    collection = unstable
                elif tools_package_name not in collection:
                    print 'Tools package {} declares its _documentation_section improperly in its __init__.'.format(
                        tools_package_name)
            elif tools_package_name not in collection:
                print 'Tools package {} does not declare a _documentation_section in its __init__.'.format(
                    tools_package_name)

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

        return composition, manual, unstable, internals
        

    ### PUBLIC PROPERTIES ###

    @property
    def code_tools_path(self):
        '''Path to Abjad tools package.'''
        from abjad import ABJCFG
        return os.path.join(ABJCFG.ABJAD_PATH, 'tools')

    @property
    def docs_api_index_path(self):
        '''Path to index.rst for Abjad API.'''
        from abjad import ABJCFG
        return os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'index.rst')

    @property
    def docs_tools_path(self):
        '''Path to tools directory inside docs.'''
        from abjad import ABJCFG
        return os.path.join(ABJCFG.ABJAD_PATH, 'docs', 'source', 'api', 'tools')

    @property
    def package_prefix(self):
        return 'abjad.tools.'

    @property
    def root_package(self):
        return 'abjad'

    @property
    def tools_package_path_index(self):
        return 2
