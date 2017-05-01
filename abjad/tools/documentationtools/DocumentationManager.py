# -*- coding: utf-8 -*-
from __future__ import print_function
import enum
import inspect
import importlib
import os
import shutil
import types
from abjad.tools import abctools
from abjad.tools import systemtools


class DocumentationManager(abctools.AbjadObject):
    r'''An API documentation manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    api_directory_name = 'api'

    api_title = 'Abjad API'

    ignored_special_methods = (
        '__dict__',
        '__getattribute__',
        '__getnewargs__',
        '__getstate__',
        '__init__',
        '__reduce__',
        '__reduce_ex__',
        '__setstate__',
        '__sizeof__',
        '__subclasshook__',
        'fromkeys',
        'pipe_cloexec',
        )

    lineage_graph_addresses = (
        'abjad',
        'abjad.tools.abjadbooktools',
        'experimental',
        'ide',
        )

    root_package_name = 'abjad'

    source_directory_path_parts = ('docs', 'source')

    tools_packages_package_path = 'abjad.tools'

    ### PRIVATE METHODS ###

    def _ensure_directory(self, path):
        path = os.path.dirname(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_api_directory_path(self, source_directory):
        if self.api_directory_name:
            path = os.path.join(
                source_directory,
                self.api_directory_name,
                )
        else:
            path = source_directory
        return path

    def _get_api_index_file_path(self, source_directory):
        if self.api_directory_name:
            directory_path = os.path.join(
                source_directory,
                self.api_directory_name,
                )
        else:
            directory_path = source_directory
        api_index_path = os.path.join(
            directory_path,
            'index.rst',
            )
        return api_index_path

    def _get_api_index_rst(self, tools_packages):
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        heading = documentationtools.ReSTHeading(
            level=2,
            text=self.api_title,
            )
        document.append(heading)
        toc = documentationtools.ReSTTOCDirective(
            options={
                'maxdepth': 3,
                'includehidden': True,
                },
            )
        for tools_package in tools_packages:
            tools_package_parts = tools_package.__name__.split('.')[1:]
            tools_package_path = '/'.join(tools_package_parts)
            text = '{}/index'
            text = text.format(tools_package_path)
            toc_item = documentationtools.ReSTTOCItem(text=text)
            toc.append(toc_item)
        document.append(toc)
        return document

    def _get_ignored_classes(self):
        from abjad.tools import abjadbooktools
        ignored_classes = set([
            abjadbooktools.abjad_import_block,
            abjadbooktools.abjad_input_block,
            abjadbooktools.abjad_output_block,
            abjadbooktools.abjad_reveal_block,
            abjadbooktools.abjad_thumbnail_block,
            systemtools.TestCase,
            ])
        return ignored_classes

    def _get_root_module(self):
        root_module = importlib.import_module(self.root_package_name)
        return root_module

    def _get_source_directory(self):
        if hasattr(self, 'docs_directory'):
            source_directory = os.path.join(self.docs_directory, 'source')
            return source_directory
        root_package = importlib.import_module(self.root_package_name)
        root_package_path = root_package.__path__[0]
        path_parts = [root_package_path]
        path_parts.extend(self.source_directory_path_parts)
        source_directory = os.path.join(*path_parts)
        return source_directory

    def _get_tools_package_contents(self, tools_package):
        classes = []
        functions = []
        for name in dir(tools_package):
            if name.startswith('_'):
                continue
            obj = getattr(tools_package, name)
            if not hasattr(obj, '__module__'):
                if getattr(obj, '__name__', None) == 'abjad':
                    pass
                else:
                    message = 'Warning: no nominative object in {}'
                    message = message.format(obj)
                    print(message)
                continue
            if not obj.__module__.startswith(tools_package.__name__):
                continue
            if isinstance(obj, type):
                classes.append(obj)
            elif isinstance(obj, types.FunctionType):
                functions.append(obj)
        classes.sort(key=lambda x: x.__name__)
        classes = tuple(classes)
        functions.sort(key=lambda x: x.__name__)
        functions = tuple(functions)
        return classes, functions

    def _get_lineage_graph_addresses(self):
        lineage_graph_addresses = set(self.lineage_graph_addresses)
        lineage_graph_addresses.add(self.root_package_name)
        lineage_graph_addresses = sorted(lineage_graph_addresses)
        return lineage_graph_addresses

    def _get_tools_package_graph(self, tools_package):
        from abjad.tools import documentationtools
        lineage_graph_addresses = self._get_lineage_graph_addresses()
        inheritance_graph = documentationtools.InheritanceGraph(
            addresses=lineage_graph_addresses,
            lineage_addresses=[tools_package.__name__]
            )
        lineage_graph = inheritance_graph.__graph__()
        lineage_graph.attributes['bgcolor'] = 'transparent'
        lineage_graph.attributes['dpi'] = 72
        lineage_graph.attributes['rankdir'] = 'LR'
        return lineage_graph

    def _build_tools_package_rst(self, tools_package):
        from abjad.tools import documentationtools
        classes, functions = self._get_tools_package_contents(
            tools_package,
            )
        document = documentationtools.ReSTDocument()
        text = tools_package.__name__.split('.')[-1]
        heading = documentationtools.ReSTHeading(level=2, text=text)
        document.append(heading)
        automodule_directive = documentationtools.ReSTAutodocDirective(
            argument=tools_package.__name__,
            directive='automodule',
            )
        document.append(automodule_directive)
        ignored_classes = self._get_ignored_classes()
        classes = [_ for _ in classes if _ not in ignored_classes]
        if classes:
            rule = documentationtools.ReSTHorizontalRule()
            document.append(rule)
            lineage_heading = documentationtools.ReSTHeading(
                level=3,
                text='Lineage',
                )
            document.append(lineage_heading)
            lineage_graph = self._get_tools_package_graph(tools_package)
            graphviz_directive = documentationtools.ReSTGraphvizDirective(
                graph=lineage_graph,
                )
            graphviz_container = documentationtools.ReSTDirective(
                directive='container',
                argument='graphviz',
                )
            graphviz_container.append(graphviz_directive)
            document.append(graphviz_container)
            sections = {}
            for cls in classes:
                documentation_section = getattr(
                    cls,
                    '__documentation_section__',
                    None,
                    )
                if documentation_section is None:
                    if issubclass(cls, enum.Enum):
                        documentation_section = 'Enumerations'
                    if issubclass(cls, Exception):
                        documentation_section = 'Errors'
                    else:
                        documentation_section = 'Classes'
                    if inspect.isabstract(cls):
                        documentation_section = 'Abstract Classes'
                if documentation_section not in sections:
                    sections[documentation_section] = []
                sections[documentation_section].append(cls)
            section_names = sorted(sections)
            if 'Main Classes' in sections:
                section_names.remove('Main Classes')
                section_names.insert(0, 'Main Classes')
            if 'Errors' in sections:
                section_names.remove('Errors')
                section_names.append('Errors')
            for section_name in section_names:
                rule = documentationtools.ReSTHorizontalRule()
                document.append(rule)
                heading = documentationtools.ReSTHeading(
                    level=3,
                    text=section_name,
                    )
                document.append(heading)
                toc = documentationtools.ReSTTOCDirective(
                    options={'hidden': True},
                    )
                for cls in sections[section_name]:
                    class_name = cls.__name__
                    if class_name == 'Index':
                        class_name = '_Index'
                    text = class_name
                    toc_item = documentationtools.ReSTTOCItem(text=text)
                    toc.append(toc_item)
                document.append(toc)
                autosummary = documentationtools.ReSTAutosummaryDirective(
                    options={'nosignatures': True},
                    )
                for cls in sections[section_name]:
                    text = cls.__name__
                    item = documentationtools.ReSTAutosummaryItem(text=text)
                    autosummary.append(item)
                document.append(autosummary)
        if functions:
            if classes:
                rule = documentationtools.ReSTHorizontalRule()
                document.append(rule)
            text = 'Functions'
            heading = documentationtools.ReSTHeading(level=3, text=text)
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective(
                options={'hidden': True},
                )
            for function in functions:
                text = function.__name__
                toc_item = documentationtools.ReSTTOCItem(text=text)
                toc.append(toc_item)
            document.append(toc)
            autosummary = documentationtools.ReSTAutosummaryDirective(
                options={'nosignatures': True},
                )
            for function in functions:
                text = function.__name__
                item = documentationtools.ReSTAutosummaryItem(text=text)
                autosummary.append(item)
            document.append(autosummary)
        return document

    def _get_tools_packages(self):
        if hasattr(self, 'packages_to_document'):
            packages_to_document = []
            package_paths = self.packages_to_document.split(',')
            for package_path in package_paths:
                package = importlib.import_module(package_path)
                packages_to_document.append(package)
            return packages_to_document
        root_module = self._get_root_module()
        if os.path.pathsep in self.tools_packages_package_path:
            tools_packages = []
            parts = self.tools_packages_package_path.split(os.path.pathsep)
            for part in parts:
                tools_packages_module = self._get_tools_packages_module(part)
                if getattr(tools_packages_module, '_is_tools_package', None):
                    tools_packages.append(tools_packages_module)
                else:
                    message = 'when passing in a list of paths all should'
                    message += ' be set with _is_tools_package=True.'
                    raise Exception(message)
            return tools_packages
        tools_packages_module = self._get_tools_packages_module()
        if getattr(tools_packages_module, '_is_tools_package', None):
            tools_packages = [tools_packages_module]
            return tools_packages
        tools_packages = []
        for name in dir(tools_packages_module):
            if name.startswith('_'):
                continue
            module = getattr(tools_packages_module, name)
            if not isinstance(module, types.ModuleType):
                continue
            if not module.__name__.startswith(root_module.__name__):
                continue
            tools_packages.append(module)
        tools_packages.sort(key=lambda x: x.__name__)
        tools_packages = tuple(tools_packages)
        return tools_packages

    def _get_tools_packages_module(self, tools_packages_package_path=None):
        if tools_packages_package_path is None:
            tools_packages_package_path = self.tools_packages_package_path
        tools_packages_module = importlib.import_module(
            tools_packages_package_path)
        return tools_packages_module

    def _module_path_to_file_path(self, module_path, source_directory):
        parts = module_path.split('.')
        parts = parts[1:]
        parts[-1] = parts[-1] + '.rst'
        parts.insert(0, self._get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    def _package_path_to_file_path(self, package_path, source_directory):
        assert isinstance(package_path, str), repr(package_path)
        parts = package_path.split('.')
        parts = parts[1:]
        parts.append('index.rst')
        parts.insert(0, self._get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    def _write(self, file_path, string, rewritten_files):
        if not string.endswith('\n'):
            string = '{}\n'.format(string)
        should_write = True
        if os.path.exists(file_path):
            with open(file_path, 'r') as file_pointer:
                old_string = file_pointer.read()
            if old_string == string:
                should_write = False
        if should_write:
            if os.path.exists(file_path):
                print('{}{}'.format(
                    self.prefix_rewrote,
                    os.path.relpath(file_path),
                    ))
            else:
                print('{}{}'.format(
                    self.prefix_wrote,
                    os.path.relpath(file_path),
                    ))
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(string)
        else:
            print('{}{}'.format(
                self.prefix_preserved,
                os.path.relpath(file_path),
                ))
        rewritten_files.add(file_path)

    ### PUBLIC METHODS ###

    def execute(self):
        r'''Executes documentation manager.
        '''
        from abjad.tools import documentationtools
        message = 'Rebuilding documentation source ...'
        print(message)
        source_directory = self._get_source_directory()
        if not os.path.exists(source_directory):
            os.makedirs(source_directory)
        static_html_directory = os.path.join(source_directory, '_static')
        if not os.path.exists(static_html_directory):
            os.makedirs(static_html_directory)
            gitignore_file = os.path.join(static_html_directory, '.gitignore')
            with open(gitignore_file, 'w') as file_pointer:
                file_pointer.write('')
        with systemtools.TemporaryDirectoryChange(
            directory=source_directory,
            verbose=True,
            ):
            rewritten_files = set()
            tools_packages = self._get_tools_packages()
            api_index_rst = self._get_api_index_rst(tools_packages)
            api_index_file_path = self._get_api_index_file_path(
                source_directory)
            self._ensure_directory(api_index_file_path)
            self._write(
                api_index_file_path,
                api_index_rst.rest_format,
                rewritten_files,
                )
            ignored_classes = self._get_ignored_classes()
            for package in tools_packages:
                tools_package_rst = self._build_tools_package_rst(package)
                tools_package_file_path = self._package_path_to_file_path(
                    package.__name__,
                    source_directory,
                    )
                self._ensure_directory(tools_package_file_path)
                self._write(
                    tools_package_file_path,
                    tools_package_rst.rest_format,
                    rewritten_files,
                    )
                classes, functions = \
                    self._get_tools_package_contents(package)
                for class_ in classes:
                    file_path = self._module_path_to_file_path(
                        class_.__module__,
                        source_directory,
                        )
                    if class_ in ignored_classes:
                        message = '{}{}'
                        message = message.format(
                            self.prefix_ignored,
                            os.path.relpath(file_path),
                            )
                        print(message)
                        continue
                    documenter = documentationtools.ClassDocumenter(
                        self, class_)
                    rst = documenter.build_rst()
                    self._write(file_path, rst.rest_format, rewritten_files)
                for function in functions:
                    file_path = self._module_path_to_file_path(
                        function.__module__,
                        source_directory,
                        )
                    documenter = documentationtools.FunctionDocumenter(
                        self, function)
                    rst = documenter.build_rst()
                    self._write(file_path, rst.rest_format, rewritten_files)
            for root, directory_names, file_names in os.walk(
                self._get_api_directory_path(source_directory),
                topdown=False,
                ):
                for file_name in file_names[:]:
                    file_path = os.path.join(root, file_name)
                    if not file_path.endswith('.rst'):
                        continue
                    if file_path not in rewritten_files:
                        file_names.remove(file_name)
                        os.remove(file_path)
                        message = '{}{}'
                        message = message.format(
                            self.prefix_pruned,
                            os.path.relpath(file_path),
                            )
                        print(message)
                if not file_names and not directory_names:
                    shutil.rmtree(root)
                    message = '{}{}'
                    message = message.format(
                        self.prefix_pruned,
                        os.path.relpath(root),
                        )
                    print(message)

    @staticmethod
    def make_readme():
        r'''Creates README.rst file.
        '''
        import abjad
        abjad_path = abjad.__path__[0]
        version = abjad.__version__
        docs_path = os.path.join(abjad_path, 'docs', 'source')
        abstract_path = os.path.join(docs_path, 'abstract.txt')
        badges_path = os.path.join(docs_path, 'badges.txt')
        links_path = os.path.join(docs_path, 'links.txt')
        installation_path = os.path.join(docs_path, 'installation.rst')
        result = 'Abjad {}'.format(version)
        result = ['#' * len(result), result, '#' * len(result)]
        with open(abstract_path, 'r') as file_pointer:
            result.append('')
            result.append(file_pointer.read())
        with open(links_path, 'r') as file_pointer:
            result.append('')
            result.append(file_pointer.read())
        with open(badges_path, 'r') as file_pointer:
            result.append('')
            result.append(file_pointer.read())
        with open(installation_path, 'r') as file_pointer:
            result.append('')
            result.append(file_pointer.read())
        result = '\n'.join(result)
        readme_path = os.path.join(abjad_path, '..', 'README.rst')
        with open(readme_path, 'w') as file_pointer:
            file_pointer.write(result)

    ### PUBLIC PROPERTIES ###

    @property
    def prefix_ignored(self):
        r'''Messaging prefix for ignored files.
        '''
        from sphinx.util.console import lightgray
        return lightgray('IGNORED:   ')

    @property
    def prefix_preserved(self):
        r'''Messaging prefix for preserved files.
        '''
        from sphinx.util.console import darkgray
        return darkgray('PRESERVED: ')

    @property
    def prefix_pruned(self):
        r'''Messaging prefix for pruned files.
        '''
        from sphinx.util.console import red
        return red('PRUNED:    ')

    @property
    def prefix_rewrote(self):
        r'''Messaging prefix for rewritten files.
        '''
        from sphinx.util.console import green
        return green('REWROTE:   ')

    @property
    def prefix_wrote(self):
        r'''Messaging prefix for written files.
        '''
        from sphinx.util.console import yellow
        return yellow('WROTE:     ')
