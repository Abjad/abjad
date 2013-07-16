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
        pass 

    ### PRIVATE METHODS ###

    def _examine_tools_package(self):
        code_root = self.obj.__path__[0]
        root_package_name = self.prefix.split('.')[0] 
        crawler = documentationtools.ModuleCrawler(
            code_root,
            root_package_name=root_package_name,
            ignored_directories=self.ignored_directories,
            )
        abstract_class_documenters = []
        concrete_class_documenters = []
        function_documenters = []
         

        self._abstract_class_documenters = tuple(sorted(
            abstract_class_documenters,
            key=lambda x: x.module_name))
        self._concrete_class_documenters = tuple(sorted(
            concrete_class_documenters,
            key=lambda x: x.module_name))
        self._function_documenters = tuple(sorted(
            function_documenters,
            key=lambda x: x.module_name))
        self._documentation_section = getattr(self.obj,
            '_documentation_section', None)

    ### PUBLIC PROPERTIES ###

    @property
    def abstract_class_documenters(self):
        return self._abstract_class_documenters

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
