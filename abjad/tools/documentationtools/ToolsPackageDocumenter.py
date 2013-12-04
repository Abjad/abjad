# -*- encoding: utf-8 -*-
import os
import types
from abjad.tools.documentationtools.Documenter import Documenter


class ToolsPackageDocumenter(Documenter):
    r'''Generates an index for every tools package.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        object_=None,
        ignored_directory_names=(),
        prefix='abjad.tools.',
        ):
        if object_ is None:
            return
        assert isinstance(object_, types.ModuleType)
        Documenter.__init__(self, object_, prefix=prefix)
        self._ignored_directory_names = ignored_directory_names
        self._examine_tools_package()

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls tools package documenter.
        
        Generates documentation:

        ::

            >>> module = scoretools
            >>> documenter = documentationtools.ToolsPackageDocumenter(
            ...     scoretools)
            >>> restructured_text = documenter()

        Returns string.
        '''
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        document.append(documentationtools.ReSTHeading(
            level=2,
            text=self._shrink_module_name(self.module_name)
            ))
        document.append(documentationtools.ReSTAutodocDirective(
            argument=self.module_name,
            directive='automodule',
            ))
        html_only = documentationtools.ReSTOnlyDirective(argument='html')
        if self.abstract_class_documenters:
            html_only.extend(self._build_autosummary_section(
                'Abstract classes',
                self.abstract_class_documenters,
                ))
        if self.concrete_class_documenters:
            html_only.extend(self._build_autosummary_section(
                'Concrete classes',
                self.concrete_class_documenters,
                ))
        if self.function_documenters:
            html_only.extend(self._build_autosummary_section(
                'Functions',
                self.function_documenters,
                ))
        document.append(html_only)
        return document.rest_format

    ### PRIVATE METHODS ###

    def _build_autosummary_section(self, banner, documenters):
        from abjad.tools import documentationtools
        result = []
        heading = documentationtools.ReSTHeading(
            level=3,
            text=banner,
            )
        result.append(heading)
        autosummary = documentationtools.ReSTAutosummaryDirective()
        for documenter in documenters:
            autosummary.append('~{}'.format(documenter.module_name))
        result.append(autosummary)
        return result

    def _examine_tools_package(self):
        from abjad.tools import documentationtools
        code_root = self.object_.__path__[0]
        root_package_name = self.prefix.split('.')[0]
        crawler = documentationtools.ModuleCrawler(
            code_root,
            root_package_name=root_package_name,
            ignored_directory_names=self.ignored_directory_names,
            )
        abstract_class_documenters = []
        concrete_class_documenters = []
        function_documenters = []
        for module in crawler:
            obj_name = module.__name__.split('.')[-1]
            if not hasattr(module, obj_name) or obj_name.startswith('_'):
                continue
            obj = getattr(module, obj_name)
            if isinstance(obj, types.TypeType):
                documenter = documentationtools.ClassDocumenter(
                    obj,
                    prefix=self.prefix,
                    )
                if documenter.is_abstract:
                    abstract_class_documenters.append(documenter)
                else:
                    concrete_class_documenters.append(documenter)
            elif isinstance(obj, types.FunctionType):
                documenter = documentationtools.FunctionDocumenter(
                    obj,
                    prefix=self.prefix,
                    )
                function_documenters.append(documenter)
        self._abstract_class_documenters = tuple(sorted(
            abstract_class_documenters,
            key=lambda x: x.module_name))
        self._concrete_class_documenters = tuple(sorted(
            concrete_class_documenters,
            key=lambda x: x.module_name))
        self._function_documenters = tuple(sorted(
            function_documenters,
            key=lambda x: x.module_name))
        self._documentation_section = getattr(self.object_,
            '_documentation_section', None)

    ### PUBLIC METHODS ###

    def create_api_toc_section(self):
        r'''Creates a TOC section to be included in the master API index.

        ::

            >>> module = scoretools
            >>> documenter = documentationtools.ToolsPackageDocumenter(module)
            >>> result = documenter.create_api_toc_section()

        Returns list.
        '''
        from abjad.tools import documentationtools
        result = []
        heading = documentationtools.ReSTHeading(
            level=2,
            text=':py:mod:`{} <{}>`'.format(
                self._shrink_module_name(self.module_name), self.module_name)
            )
        result.append(heading)

        only_html = documentationtools.ReSTOnlyDirective(argument='html')
        only_latex = documentationtools.ReSTOnlyDirective(argument='latex')

        hidden_toc = documentationtools.ReSTTOCDirective(
            options={
                'hidden': True,
                'maxdepth': 1,
                },
            )
        index_path = '/'.join(self.module_name.split('.')[1:] + ['index'])
        hidden_toc.append(index_path)
        only_html.append(hidden_toc)

        def module_name_to_toc_entry(module_name):
            return '/'.join(module_name.split('.')[1:-1])

        def make_subsection(banner, documenters, only_html, only_latex):
            only_latex.append(documentationtools.ReSTHeading(
                level=3,
                text=banner
                ))
            toc_html = documentationtools.ReSTTOCDirective(
                options={'maxdepth': 1},
                )
            toc_latex = documentationtools.ReSTTOCDirective()
            for documenter in documenters:
                toc_entry = module_name_to_toc_entry(
                    documenter.module_name)
                toc_html.append(toc_entry)
                toc_latex.append(toc_entry)
            only_html.append(toc_html)
            only_latex.append(toc_latex)

        if self.abstract_class_documenters:
            make_subsection(
                'Abstract classes',
                self.abstract_class_documenters,
                only_html,
                only_latex,
                )
        if self.concrete_class_documenters:
            make_subsection(
                'Concrete classes',
                self.concrete_class_documenters,
                only_html,
                only_latex,
                )
        if self.function_documenters:
            make_subsection(
                'Functions',
                self.function_documenters,
                only_html,
                only_latex,
                )
        result.extend((only_html, only_latex))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def abstract_class_documenters(self):
        r'''Abstract class documenters.
        '''
        return self._abstract_class_documenters

    @property
    def all_documenters(self):
        r'''All documenters.
        '''
        return self.abstract_class_documenters + \
            self.concrete_class_documenters + \
            self.function_documenters

    @property
    def concrete_class_documenters(self):
        r'''Concrete class documenters.
        '''
        return self._concrete_class_documenters

    @property
    def documentation_section(self):
        r'''Documentation section.
        '''
        return self._documentation_section

    @property
    def function_documenters(self):
        r'''Function documenters.
        '''
        return self._function_documenters

    @property
    def ignored_directory_names(self):
        r'''Ignored directory names.
        '''
        return self._ignored_directory_names

    @property
    def module_name(self):
        r'''Module name.

        Returns string.
        '''
        return self.object_.__name__
