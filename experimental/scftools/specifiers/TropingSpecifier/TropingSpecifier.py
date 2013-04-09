from scftools.specifiers.ParameterSpecifier import ParameterSpecifier


class TropingSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, troping_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.troping_handler_name = troping_handler_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.troping_handler_name
