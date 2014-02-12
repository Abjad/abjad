# -*- encoding: utf-8 -*-
from scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class StaffSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self,
        description=None,
        staff_handler_name=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.staff_handler_name = staff_handler_name

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.staff_handler_name
