from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class DirectiveSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, directive_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.directive_handler_name = directive_handler_name

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.directive_handler_name
