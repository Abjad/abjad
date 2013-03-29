from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class OverrideSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, override_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.override_handler_name = override_handler_name

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.override_handler_name
