import os
from abjad.cfg.cfg import ABJADPATH
from abjad.tools import abctools
from abjad.tools.documentationtools.APICrawler import APICrawler


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
        'sequencetools',
        'sievetools',
        'tempotools',
        'threadtools',
        'timeintervaltools',
        'timesignaturetools',
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
        for package_name in sorted(composition.keys()):
            result.extend(self._create_package_title(package_name))
            for module_name in composition[package_name]:
                result.append('   %s' % self._module_name_to_toc_entry(module_name))
            result.append('')

        # manually loading composition packages
        result.extend(self._create_section_title(self._manual_packages_description))
        for package_name in sorted(manual.keys()):
            result.extend(self._create_package_title(package_name))
            for module_name in manual[package_name]:
                result.append('   %s' % self._module_name_to_toc_entry(module_name))
            result.append('')

        # unstable composition packages
        result.extend(self._create_section_title(self._unstable_packages_description))
        for package_name in sorted(unstable.keys()):
            result.extend(self._create_package_title(package_name))
            for module_name in unstable[package_name]:
                result.append('   %s' % self._module_name_to_toc_entry(module_name))
            result.append('')

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
        return [
            package_name,
            '',
            '.. toctree::',
            '   :maxdepth: 1',
            ''
        ]

    def _create_section_title(self, title):
        result = self._create_heading(title, '-')
        result.extend([
            '.. toctree::',
            '   :maxdepth: 1',
            ''
        ])
        return result

    def _module_name_to_toc_entry(self, module_name):
        parts = module_name.split('.')[1:]
        return '/'.join(parts)

    def _sort_modules(self, module_names):
        composition = {}
        manual = {}
        unstable = {}

        for module_name in module_names:
            tools_package = module_name.split('.')[2]

            if tools_package in self._undocumented_packages:
                continue

            if tools_package in self._unstable_packages:
                if tools_package not in unstable:
                    unstable[tools_package] = []
                unstable[tools_package].append(module_name)

            elif tools_package in self._manual_packages:
                if tools_package not in manual:
                    manual[tools_package] = []
                manual[tools_package].append(module_name)

            else:
                if tools_package not in composition:
                    composition[tools_package] = []
                composition[tools_package].append(module_name)

        for d in (composition, manual, unstable):
            for k, v in d.iteritems():
                d[k] = sorted(v)
                     
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
