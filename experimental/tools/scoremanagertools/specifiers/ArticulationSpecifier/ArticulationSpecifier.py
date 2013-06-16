from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class ArticulationSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, articulation_handler_name=None, description=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.articulation_handler_name = articulation_handler_name

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.name or self.articulation_handler_name
