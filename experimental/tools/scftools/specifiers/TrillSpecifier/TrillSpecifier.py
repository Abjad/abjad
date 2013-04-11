from experimental.tools.scftools.specifiers.ParameterSpecifier import ParameterSpecifier


class TrillSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, trill_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.trill_handler_name = trill_handler_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.trill_handler_name
