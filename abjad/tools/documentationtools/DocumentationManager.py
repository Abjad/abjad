# -*- encoding: utf-8 -*-
from __future__ import print_function
import enum
import inspect
import importlib
import os
import re
import shutil
import traceback
import types
from abjad.tools import abctools
from abjad.tools import systemtools
from sphinx.util.console import red, green, darkgray, lightgray, yellow


class DocumentationManager(abctools.AbjadObject):
    r'''An API documentation manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    api_directory_name = 'api'
    api_title = 'Abjad API'
    root_package_name = 'abjad'
    source_directory_path_parts = ('docs', 'source')
    tools_packages_package_path = 'abjad.tools'

    prefix_ignored = lightgray('IGNORED:   ')
    prefix_preserved = darkgray('PRESERVED: ')
    prefix_pruned = red('PRUNED:    ')
    prefix_rewrote = green('REWROTE:   ')
    prefix_wrote = yellow('WROTE:     ')

    ### PRIVATE METHODS ###

    def _build_attribute_section(
        self,
        cls,
        attrs,
        directive,
        title,
        ):
        r'''
        '''
        from abjad.tools import documentationtools
        result = []
        if attrs:
            result.append(documentationtools.ReSTHeading(
                level=3,
                text=title,
                ))
            for attr in attrs:
                options = {
                    'noindex': True,
                    }
                autodoc = documentationtools.ReSTAutodocDirective(
                    argument='{}.{}'.format(cls.__name__, attr.name),
                    directive=directive,
                    options=options,
                    )
                if cls is attr.defining_class:
                    result.append(autodoc)
                else:
                    container = documentationtools.ReSTDirective(
                        argument='inherited',
                        directive='container',
                        )
                    container.append(autodoc)
                    html_only = documentationtools.ReSTDirective(
                        argument='html',
                        directive='only',
                        )
                    html_only.append(container)
                    result.append(html_only)
        return result

    def _build_attributes_autosummary(
        self,
        cls,
        class_methods,
        data,
        inherited_attributes,
        methods,
        readonly_properties,
        readwrite_properties,
        special_methods,
        static_methods,
        ):
        r'''
        '''
        from abjad.tools import documentationtools
        result = []
        attributes = []
        attributes.extend(readonly_properties)
        attributes.extend(readwrite_properties)
        attributes.extend(methods)
        attributes.extend(class_methods)
        attributes.extend(static_methods)
        attributes.sort(key=lambda x: x.name)
        attributes.extend(special_methods)
        if attributes:
            autosummary = documentationtools.ReSTAutosummaryDirective()
            for attribute in attributes:
                autosummary.append('~{}.{}.{}'.format(
                    cls.__module__,
                    cls.__name__,
                    attribute.name,
                    ))
            html_only = documentationtools.ReSTOnlyDirective(argument='html')
            html_only.append(documentationtools.ReSTHeading(
                level=3,
                text='Attribute summary',
                ))
            html_only.append(autosummary)
            result.append(html_only)
        return result

    def _build_bases_section(self, cls):
        from abjad.tools import documentationtools
        result = []
        result.append(documentationtools.ReSTHeading(
            level=3,
            text='Bases',
            ))
        mro = inspect.getmro(cls)[1:]
        for cls in mro:
            parts = cls.__module__.split('.') + [cls.__name__]
            while 1 < len(parts) and parts[-1] == parts[-2]:
                parts.pop()
            packagesystem_path = '.'.join(parts)
            text = '- :py:class:`{}`'.format(packagesystem_path)
            paragraph = documentationtools.ReSTParagraph(
                text=text,
                wrap=False,
                )
            result.append(paragraph)
        return result

    def _build_enumeration_section(self, cls):
        from abjad.tools import documentationtools
        result = []
        if not issubclass(cls, enum.Enum):
            return result
        items = sorted(cls, key=lambda x: x.name)
        if items:
            result.append(documentationtools.ReSTHeading(
                level=3,
                text='Enumeration Items',
                ))
            for item in items:
                name = item.name
                value = item.value
                line = '- `{}`: {}'.format(name, value)
                paragraph = documentationtools.ReSTParagraph(
                    text=line,
                    wrap=False,
                    )
                result.append(paragraph)
        return result

    def _collect_class_attributes(self, cls):
        ignored_special_methods = (
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
        class_methods = []
        data = []
        inherited_attributes = []
        methods = []
        readonly_properties = []
        readwrite_properties = []
        special_methods = []
        static_methods = []
        attrs = inspect.classify_class_attrs(cls)
        for attr in attrs:
            if attr.defining_class is object:
                continue
            if attr.defining_class is not cls:
                inherited_attributes.append(attr)
            if attr.kind == 'method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        methods.append(attr)
            elif attr.kind == 'class method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        class_methods.append(attr)
            elif attr.kind == 'static method':
                if attr.name not in ignored_special_methods:
                    if attr.name.startswith('__'):
                        special_methods.append(attr)
                    elif not attr.name.startswith('_'):
                        static_methods.append(attr)
            elif attr.kind == 'property' and not attr.name.startswith('_'):
                if attr.object.fset is None:
                    readonly_properties.append(attr)
                else:
                    readwrite_properties.append(attr)
            elif attr.kind == 'data' and not attr.name.startswith('_') \
                and attr.name not in getattr(cls, '__slots__', ()):
                data.append(attr)
        class_methods = tuple(sorted(class_methods))
        data = tuple(sorted(data))
        inherited_attributes = tuple(sorted(inherited_attributes))
        methods = tuple(sorted(methods))
        readonly_properties = tuple(sorted(readonly_properties))
        readwrite_properties = tuple(sorted(readwrite_properties))
        special_methods = tuple(sorted(special_methods))
        static_methods = tuple(sorted(static_methods))
        result = (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            )
        return result

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
        r'''
        '''
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
            tools_package_parts = tools_package.__package__.split('.')[1:]
            tools_package_path = '/'.join(tools_package_parts)
            toc_item = documentationtools.ReSTTOCItem(
                text='{}/index'.format(tools_package_path),
                )
            toc.append(toc_item)
        document.append(toc)
        return document

    def _get_class_rst(self, cls):
        import abjad
        module_name, _, class_name = cls.__module__.rpartition('.')
        tools_package_python_path = '.'.join(cls.__module__.split('.')[:-1])
        (
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ) = self._collect_class_attributes(cls)
        document = abjad.documentationtools.ReSTDocument()
        module_directive = abjad.documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=class_name,
            )
        document.append(heading)
        autoclass_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=cls.__name__,
            directive='autoclass',
            )
        document.append(autoclass_directive)
        try:
            lineage_heading = abjad.documentationtools.ReSTHeading(
                level=3,
                text='Lineage',
                )
            document.append(lineage_heading)
            lineage_graph = self._get_lineage_graph(cls)
            lineage_graph.attributes['background'] = 'transparent'
            lineage_graph.attributes['rankdir'] = 'LR'
            graphviz_directive = \
                abjad.documentationtools.ReSTGraphvizDirective(
                    graph=lineage_graph,
                    )
            graphviz_container = abjad.documentationtools.ReSTDirective(
                directive='container',
                argument='graphviz',
                )
            graphviz_container.append(graphviz_directive)
            document.append(graphviz_container)
        except:
            traceback.print_exc()
        document.extend(self._build_bases_section(cls))
        document.extend(self._build_enumeration_section(cls))
        document.extend(self._build_attributes_autosummary(
            cls,
            class_methods,
            data,
            inherited_attributes,
            methods,
            readonly_properties,
            readwrite_properties,
            special_methods,
            static_methods,
            ))
        document.extend(self._build_attribute_section(
            cls,
            readonly_properties,
            'autoattribute',
            'Read-only properties',
            ))
        document.extend(self._build_attribute_section(
            cls,
            readwrite_properties,
            'autoattribute',
            'Read/write properties',
            ))
        document.extend(self._build_attribute_section(
            cls,
            methods,
            'automethod',
            'Methods',
            ))
        document.extend(self._build_attribute_section(
            cls,
            sorted(class_methods + static_methods,
                key=lambda x: x.name,
                ),
            'automethod',
            'Class & static methods',
            ))
#        document.extend(self._build_attribute_section(
#            cls,
#            class_methods,
#            'automethod',
#            'Class methods',
#            ))
#        document.extend(self._build_attribute_section(
#            cls,
#            static_methods,
#            'automethod',
#            'Static methods',
#            ))
        document.extend(self._build_attribute_section(
            cls,
            special_methods,
            'automethod',
            'Special methods',
            ))
        return document

    def _get_class_summary(self, cls):
        r'''
        '''
        doc = cls.__doc__
        if doc is None:
            doc = ''
        doc = doc.splitlines()
        m = re.search(r"^([A-Z].*?\.)(?:\s|$)", " ".join(doc).strip())
        if m:
            summary = m.group(1).strip()
        elif doc:
            summary = doc[0].strip()
        else:
            summary = ''
        return summary

    def _get_function_rst(self, function):
        r'''
        '''
        import abjad
        document = abjad.documentationtools.ReSTDocument()
        tools_package_python_path = '.'.join(function.__module__.split('.')[:-1])
        module_directive = abjad.documentationtools.ReSTDirective(
            directive='currentmodule',
            argument=tools_package_python_path,
            )
        document.append(module_directive)
        heading = abjad.documentationtools.ReSTHeading(
            level=2,
            text=function.__name__,
            )
        document.append(heading)
        autodoc_directive = abjad.documentationtools.ReSTAutodocDirective(
            argument=function.__name__,
            directive='autofunction',
            )
        document.append(autodoc_directive)
        return document

    def _get_ignored_classes(self):
        from abjad.tools import abjadbooktools
        ignored_classes = set([
            abjadbooktools.abjad_import_block,
            abjadbooktools.abjad_input_block,
            abjadbooktools.abjad_output_block,
            abjadbooktools.abjad_thumbnail_block,
            ])
        return ignored_classes

    def _get_tools_package_graph(self, tools_package):
        from abjad.tools import documentationtools
        inheritance_graph = documentationtools.InheritanceGraph(
            lineage_addresses=[tools_package.__package__]
            )
        lineage_graph = inheritance_graph.__graph__()
        lineage_graph.attributes['background'] = 'transparent'
        lineage_graph.attributes['rankdir'] = 'LR'
        return lineage_graph

    def _get_lineage_graph(self, cls):
        def get_node_name(original_name):
            parts = original_name.split('.')
            name = [parts[0]]
            for part in parts[1:]:
                if part != name[-1]:
                    name.append(part)
            if name[0] in ('abjad', 'experimental', 'ide'):
                return str('.'.join(name[2:]))
            return str('.'.join(name))
        from abjad.tools import documentationtools
        addresses = ('abjad', 'experimental', 'ide')
        module_name, _, class_name = cls.__module__.rpartition('.')
        node_name = get_node_name(module_name + '.' + class_name)
        importlib.import_module(module_name)
        lineage = documentationtools.InheritanceGraph(
            addresses=addresses,
            lineage_addresses=((module_name, class_name),)
            )
        graph = lineage.__graph__()
        maximum_node_count = 30
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=2,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=1,
                )
            graph = lineage.__graph__()
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            graph = lineage.__graph__()
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')
        graph_node = graph[node_name]
        graph_node.attributes['label'] = \
            '<<B>{}</B>>'.format(graph_node.attributes['label'])
        return graph

    def _get_source_directory(self):
        root_package = importlib.import_module(self.root_package_name)
        root_package_path = root_package.__path__[0]
        path_parts = [root_package_path]
        path_parts.extend(self.source_directory_path_parts)
        source_directory = os.path.join(*path_parts)
        return source_directory

    def _get_tools_packages(self):
        r'''
        '''
        root_module = self._get_root_module()
        tools_packages_module = self._get_tools_packages_module()
        tools_packages = []
        for name in dir(tools_packages_module):
            if name.startswith('_'):
                continue
            module = getattr(tools_packages_module, name)
            if not isinstance(module, types.ModuleType):
                continue
            if not module.__package__.startswith(root_module.__package__):
                continue
            tools_packages.append(module)
        tools_packages.sort(key=lambda x: x.__name__)
        tools_packages = tuple(tools_packages)
        return tools_packages

    def _get_root_module(self):
        r'''
        '''
        root_module = importlib.import_module(self.root_package_name)
        return root_module

    def _get_tools_packages_module(self):
        r'''
        '''
        tools_packages_module = importlib.import_module(
            self.tools_packages_package_path)
        return tools_packages_module

    def _get_tools_package_contents(self, tools_package):
        r'''
        '''
        classes = []
        functions = []
        for name in dir(tools_package):
            if name.startswith('_'):
                continue
            obj = getattr(tools_package, name)
            if not hasattr(obj, '__module__'):
                print('Warning: no nominative object in {}'.format(obj))
                continue
            if not obj.__module__.startswith(tools_package.__package__):
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

    def _get_tools_package_rst(self, tools_package):
        r'''
        '''
        from abjad.tools import documentationtools
        classes, functions = self._get_tools_package_contents(
            tools_package,
            )
        document = documentationtools.ReSTDocument()
        heading = documentationtools.ReSTHeading(
            level=2,
            text=tools_package.__name__.split('.')[-1],
            )
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
        if classes:
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
                    elif issubclass(cls, Exception):
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
                #heading = documentationtools.ReSTDirective(
                #    directive='rubric',
                #    argument=section_name,
                #    )
                document.append(heading)
                toc = documentationtools.ReSTTOCDirective(
                    options={
                        #'caption': section_name,
                        'hidden': True,
                        #'name': '{}__{}'.format(
                        #    tools_package.__name__,
                        #    section_name,
                        #    ),
                        },
                    )
                for cls in sections[section_name]:
                    class_name = cls.__name__
                    if class_name == 'Index':
                        class_name = '_Index'
                    toc_item = documentationtools.ReSTTOCItem(
                        text=class_name,
                        )
                    toc.append(toc_item)
                document.append(toc)
                autosummary = documentationtools.ReSTAutosummaryDirective(
                    options={
                        'nosignatures': True,
                        },
                    )
                for cls in sections[section_name]:
                    item = documentationtools.ReSTAutosummaryItem(
                        text=cls.__name__,
                        )
                    autosummary.append(item)
                document.append(autosummary)
        if functions:
            if classes:
                rule = documentationtools.ReSTHorizontalRule()
                document.append(rule)
            section_name = 'Functions'
            heading = documentationtools.ReSTHeading(
                level=3,
                text=section_name,
                )
            #heading = documentationtools.ReSTDirective(
            #    directive='rubric',
            #    argument=section_name,
            #    )
            document.append(heading)
            toc = documentationtools.ReSTTOCDirective(
                options={
                    #'caption': section_name,
                    'hidden': True,
                    #'name': '{}__{}'.format(
                    #    tools_package.__name__,
                    #    section_name,
                    #    ),
                    },
                )
            for function in functions:
                toc_item = documentationtools.ReSTTOCItem(
                    text=function.__name__,
                    )
                toc.append(toc_item)
            document.append(toc)
            autosummary = documentationtools.ReSTAutosummaryDirective(
                options={
                    'nosignatures': True,
                    },
                )
            for function in functions:
                item = documentationtools.ReSTAutosummaryItem(
                    text=function.__name__,
                    )
                autosummary.append(item)
            document.append(autosummary)
        return document

    def _module_path_to_file_path(self, module_path, source_directory):
        r'''
        '''
        parts = module_path.split('.')
        parts = parts[1:]
        if parts[-1] == 'Index':
            parts[-1] = '_' + parts[-1] + '.rst'
        else:
            parts[-1] = parts[-1] + '.rst'
        parts.insert(0, self._get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    def _package_path_to_file_path(self, package_path, source_directory):
        r'''
        '''
        parts = package_path.split('.')
        parts = parts[1:]
        parts.append('index.rst')
        parts.insert(0, self._get_api_directory_path(source_directory))
        path = os.path.join(*parts)
        return path

    def _remove_api_directory(self):
        r'''
        '''
        path = self._get_api_directory_path()
        if os.path.exists(path):
            shutil.rmtree(path)

    def _write(self, file_path, string, rewritten_files):
        r'''
        '''
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
        print('Rebuilding documentation source.')
        source_directory = self._get_source_directory()
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
                tools_package_rst = self._get_tools_package_rst(package)
                tools_package_file_path = self._package_path_to_file_path(
                    package.__package__,
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
                for cls in classes:
                    file_path = self._module_path_to_file_path(
                        cls.__module__,
                        source_directory,
                        )
                    if cls in ignored_classes:
                        print('{}{}'.format(
                            self.prefix_ignored,
                            os.path.relpath(file_path),
                            ))
                        continue
                    rst = self._get_class_rst(cls)
                    self._write(file_path, rst.rest_format, rewritten_files)
                for function in functions:
                    file_path = self._module_path_to_file_path(
                        function.__module__,
                        source_directory,
                        )
                    rst = self._get_function_rst(function)
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
                        print('{}{}'.format(
                            self.prefix_pruned,
                            os.path.relpath(file_path),
                            ))
                if not file_names and not directory_names:
                    shutil.rmtree(root)
                    print('{}{}'.format(
                        self.prefix_pruned,
                        os.path.relpath(root),
                        ))

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