from abjad.tools.documentationtools.Documenter import Documenter


class ToolsPackageDocumenter(Documenter):
    '''Generates an index for every tools package.'''

    ### PUBLIC PROPERTIES ###

    @property
    def module_name(self):
        return self.object.__path__
