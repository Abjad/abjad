from experimental.tools.scoremanagementtools.specifiers.ParameterSpecifier import ParameterSpecifier


class StaffSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, staff_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.staff_handler_name = staff_handler_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.staff_handler_name
