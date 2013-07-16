import os
import types
from abjad.tools.documentationtools.Documenter import Documenter


class ToolsPackageDocumenter(Documenter):
    '''Generates an index for every tools package.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        obj,
        prefix='abjad.tools.',
        ):
        assert isinstance(obj, types.ModuleType)
        Documenter.__init__(self, obj, prefix=prefix)
        self._examine_tools_package()

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Generate documentation:

        ::

            >>> module = notetools
            >>> documenter = documentationtools.ToolsPackageDocumenter(
            ...     notetools)
            >>> restructured_text = documenter()

        Return string.
        '''
        from abjad.tools import documentationtools 
        stripped_class_name = self._shrink_module_name(self.object.__path__[0])
        document = documentationtools.ReSTDocument()
        document.append(documentationtools.ReSTHeading(
            level=2,
            text=stripped_class_name,
            ))
        document.append(documentationtools.ReSTAutodocDirective(
            argument=self.module_name,
            directive='automodule',
            ))
        if self.abstract_class_documenters:
            document.extend(self._build_autosummary_section(
                'Abstract classes',
                self.abstract_class_documenters,
                ))
        if self.concrete_class_documenters:
            document.extend(self._build_autosummary_section(
                'Concrete classes',
                self.concrete_class_documenters,
                ))
        if self.function_documenters:
            document.extend(self._build_autosummary_section(
                'Functions',
                self.function_documenters,
                ))
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
        return result

    def _examine_tools_package(self):
        from abjad.tools import documentationtools
        code_root = self.object.__path__[0]
        root_package_name = self.prefix.split('.')[0] 
        crawler = documentationtools.ModuleCrawler(
            code_root,
            root_package_name=root_package_name,
            ignored_directories=self.ignored_directories,
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
        self._documentation_section = getattr(self.object,
            '_documentation_section', None)

    ### PUBLIC PROPERTIES ###

    @property
    def abstract_class_documenters(self):
        return self._abstract_class_documenters

    @property
    def all_documenters(self):
        return self.abstract_class_documenters + \
            self.concrete_class_documenters + \
            self.function_documenters

    @property
    def concrete_class_documenters(self):
        return self._concrete_class_documenters

    @property
    def documentation_section(self):
        return self._documentation_section

    @property
    def function_documenters(self):
        return self._function_documenters

    @property
    def module_name(self):
        return self.object.__path__
