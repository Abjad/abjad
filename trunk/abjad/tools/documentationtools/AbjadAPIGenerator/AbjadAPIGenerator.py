import os
from abjad.cfg.cfg import ABJADPATH
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

    _composition_packages_description = 'Abjad composition packages'

    _manual_packages_description = 'Additional Abjad composition packages (load manually)'

    _manual_packages = (
        'abctools',
        'configurationtools',
        'datastructuretools',
        'decoratortools',
        'documentationtools',
        'durationtools',
        'iotools',
        'layouttools',
        'lilypondparsertools',
        'mathtools',
        'pitcharraytools',
        'rhythmtreetools',
        'sequencetools',
        'sievetools',
        'tempotools',
        'threadtools',
        'timeintervaltools',
        'timesignaturetools',
        'timetokentools',
        'verticalitytools',
        'wellformednesstools'
    )

    _undocumented_packages = (
        'lilypondproxytools',
    )

    _unstable_packages_description = 'Unstable Abjad composition packages (load manually)'

    _unstable_packages = (
        'constrainttools',
        'lyricstools',
        'quantizationtools',
        'tonalitytools',
    )
    
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
        tools_crawler = APICrawler(self.code_tools_path, self.docs_tools_path, 'abjad',
            ignored_directories = ignored_directories)
        visited_modules = tools_crawler()

        composition, manual, unstable = self._sort_modules(visited_modules)

        if verbose:
            print 'Now making API index ...'

        result = []

        result.extend(self._create_heading(self._api_title))

        # automatically loading composition packages
        result.extend(self._create_section_title(self._composition_packages_description))
        for package_name in sorted(composition):
            result.extend(self._create_package_toc(package_name, composition[package_name]))

        # manually loading composition packages
        result.extend(self._create_section_title(self._manual_packages_description))
        for package_name in sorted(manual):
            result.extend(self._create_package_toc(package_name, manual[package_name]))

        # unstable composition packages
        result.extend(self._create_section_title(self._unstable_packages_description))
        for package_name in sorted(unstable):
            result.extend(self._create_package_toc(package_name, unstable[package_name]))

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
        result = self._create_heading(':py:mod:`%s <abjad.tools.%s>`' % 
            (package_name, package_name), '~')
        return result

    def _create_package_toc(self, package_name, package_modules):
        result = []
        result.extend(self._create_package_title(package_name))
        if package_modules['abstract_classes']:
            result.append('.. rubric:: %s abstract classes\n' % package_name)
            result.extend(self._create_toc_directive())
            for obj in package_modules['abstract_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')
        if package_modules['concrete_classes']:
            result.append('.. rubric:: %s concrete classes\n' % package_name)
            result.extend(self._create_toc_directive())
            for obj in package_modules['concrete_classes']:
                result.append(self._module_name_to_toc_entry(obj.module_name))
            result.append('')
        if package_modules['functions']:
            result.append('.. rubric:: %s functions\n' % package_name)
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
        parts = module_name.split('.')[1:-1]
        return '   %s' % '/'.join(parts)

    def _sort_modules(self, objects):
        composition = {}
        manual = {}
        unstable = {}

        for obj in sorted(objects, key=lambda x: x.module_name):
            tools_package = obj.module_name.split('.')[2]

            collection = None

            if tools_package in self._undocumented_packages:
                continue
            elif tools_package in self._unstable_packages:
                collection = unstable
            elif tools_package in self._manual_packages:
                collection = manual
            else:
                collection = composition

            if tools_package not in collection:
                collection[tools_package] = {
                    'abstract_classes': [],
                    'concrete_classes': [],
                    'functions': []
                }

            if isinstance(obj, ClassDocumenter):
                if obj.is_abstract:
                    collection[tools_package]['abstract_classes'].append(obj)
                else:
                    collection[tools_package]['concrete_classes'].append(obj)
            else:
                collection[tools_package]['functions'].append(obj)

        return composition, manual, unstable
        

    ### PUBLIC ATTRIBUTES ###

    @property
    def code_tools_path(self):
        '''Path to Abjad tools package.'''
        return os.path.join(ABJADPATH, 'tools')

    @property
    def docs_api_index_path(self):
        '''Path to index.rst for Abjad API.'''
        return os.path.join(ABJADPATH, 'docs', 'chapters', 'api', 'index.rst')

    @property
    def docs_tools_path(self):
        '''Path to tools directory inside docs.'''
        return os.path.join(ABJADPATH, 'docs', 'chapters', 'api', 'tools')
