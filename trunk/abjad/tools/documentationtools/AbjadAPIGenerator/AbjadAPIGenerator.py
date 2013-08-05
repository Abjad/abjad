# -*- encoding: utf-8 -*-
import importlib
import os
import shutil
from abjad.tools import abctools


class AbjadAPIGenerator(abctools.AbjadObject):
    r'''Creates Abjad's API ReST:

        * writes ReST pages for individual classes and functions
        * writes the API index ReST
        * handles sorting tools packages into composition, manual-loading 
          and unstable
        * handles ignoring private tools packages

    Returns `AbjadAPIGenerator` instance.
    '''

    ### CLASS VARIABLES ###

    _api_title = 'Abjad API'

    _package_descriptions = {
        'core': 'Core composition packages',
        'demos': 'Demos and example packages',
        'internals': 'Abjad internal packages',
        'unstable': 'Unstable packages (load manually)',
    }

    _undocumented_packages = (
        'materialpackages',
        'scorepackages',
    )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, verbose=False):
        from abjad.tools import documentationtools

        if verbose:
            print 'Now writing ReStructured Text files ...'
            print

        ignored_directory_names = ['.svn', 'test', '__pycache__']
        ignored_directory_names.extend(self._undocumented_packages)

        document = documentationtools.ReSTDocument()
        document.append(documentationtools.ReSTHeading(
            level=0,
            text=self._api_title,
            ))

        documentation_sections = {}
        for code_path, docs_path, package_prefix in self.path_definitions:
            if not os.path.exists(code_path):
                os.makedirs(code_path)
            if not os.path.exists(docs_path):
                os.makedirs(docs_path)
            self._prune_obsolete_documents(code_path, docs_path)
            for name in os.listdir(code_path):
                if name in ignored_directory_names:
                    continue
                path = os.path.join(code_path, name)
                if not os.path.isdir(path):
                    continue
                if not os.path.exists(os.path.join(
                    path, '__init__.py')):
                    continue
                packagesystem_path = ''.join((package_prefix, name))
                module = importlib.import_module(packagesystem_path)
                documenter = documentationtools.ToolsPackageDocumenter(
                    module,
                    ignored_directory_names=ignored_directory_names,
                    prefix=package_prefix,
                    )
                if not documenter.all_documenters:
                    continue
                section = documenter.documentation_section
                if section not in documentation_sections:
                    documentation_sections[section] = []
                payload = (documenter, code_path, docs_path, package_prefix)
                documentation_sections[section].append(payload)

        for section in sorted(documentation_sections):
            documenters = sorted(documentation_sections[section],
                key=lambda x: x[0].module_name)
            section_heading = documentationtools.ReSTHeading(
                level=1,
                text=self._package_descriptions.get(section,
                    'Undefinited documentation section'),
                )
            document.append(section_heading)
            for payload in documenters:
                tools_package_documenter, code_path, docs_path, package_prefix = \
                    payload
                document.extend(
                    tools_package_documenter.create_api_toc_section())
                self._write_document(tools_package_documenter,
                    code_path, docs_path, package_prefix)
                for documenter in tools_package_documenter.all_documenters:
                    self._write_document(documenter,
                        code_path, docs_path, package_prefix)
                
        documentationtools.Documenter.write(
            self.docs_api_index_path,
            document.rest_format,
            )

        if verbose:
            #print ''
            print '... done.'
            print ''

    ### PRIVATE METHODS ###

    def _prune_obsolete_documents(self, code_path, docs_path):
        for directory_path, directory_names, file_names in os.walk(docs_path):
            path_suffix = os.path.relpath(directory_path, docs_path)
            for file_name in file_names:
                if not file_name.endswith('.rst') or file_name == 'index.rst':
                    continue
                code_file_path = os.path.join(
                    code_path,
                    path_suffix,
                    file_name.replace('.rst', '.py'),
                    )
                if not os.path.exists(code_file_path):
                    docs_file_path = os.path.join(
                        directory_path,
                        file_name,
                        )
                    os.remove(docs_file_path)
                    print 'PRUNING', os.path.relpath(docs_file_path)
            for directory_name in directory_names:
                code_directory_path = os.path.join(
                    code_path,
                    path_suffix,
                    directory_name,
                    )
                if not os.path.exists(code_directory_path):
                    docs_directory_path = os.path.join(
                        directory_path,
                        directory_name,
                        )
                    shutil.rmtree(docs_directory_path)
                    print 'PRUNING', os.path.relpath(docs_directory_path)

    def _write_document(self, documenter, code_path, docs_path, package_prefix):
        from abjad.tools import documentationtools
#        print
#        print documenter.module_name
#        print docs_path
#        print package_prefix
        parts = documenter.module_name.replace(
            package_prefix, '', 1).split('.')
#        print parts
        if isinstance(documenter, documentationtools.ToolsPackageDocumenter):
            parts.append('index.rst')
        elif isinstance(documenter, (documentationtools.ClassDocumenter,
            documentationtools.FunctionDocumenter)):
            parts.pop()
            parts[-1] += '.rst'
        parts.insert(0, docs_path)
        file_path = os.path.join(*parts)
#        print file_path
        directory_path = os.path.dirname(file_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        documenter.write(file_path, documenter())

    ### PUBLIC PROPERTIES ###

    @property
    def docs_api_index_path(self):
        r'''Path to index.rst for Abjad API.
        '''
        from abjad import abjad_configuration
        return os.path.join(
            abjad_configuration.abjad_directory_path, 
            'docs', 'source', 'api', 'index.rst')

    @property
    def package_prefix(self):
        return ('abjad.tools.', 'abjad.demos.')

    @property
    def path_definitions(self):
        r'''Code path / docs path / package prefix triples.
        '''
        from abjad import abjad_configuration
        return (
            (
                os.path.join(
                    abjad_configuration.abjad_directory_path, 'tools'),
                os.path.join(
                    abjad_configuration.abjad_directory_path, 
                    'docs', 'source', 'api', 'tools'),
                'abjad.tools.',
            ),
            (
                os.path.join(
                    abjad_configuration.abjad_directory_path, 'demos'),
                os.path.join(
                    abjad_configuration.abjad_directory_path, 
                    'docs', 'source', 'api', 'demos'),
                'abjad.demos.',
            ),
        )

    @property
    def root_package(self):
        return 'abjad'

    @property
    def tools_package_path_index(self):
        return 2
