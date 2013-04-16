from experimental.tools.scoremanagementtools.specifiers.ParameterSpecifier import ParameterSpecifier


class RegistrationSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, registration_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.registration_handler_name = registration_handler_name

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.registration_handler_name
