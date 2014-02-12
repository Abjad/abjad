# -*- encoding: utf-8 -*-
from scoremanager.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class PerformerSpecifier(ParameterSpecifier):

    def __init__(
        self,
        description=None,
        custom_identifier=None,
        performer=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.performer = performer

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        if self.custom_identifier:
            return self.custom_identifier
        elif self.performer:
            return self.performer.name
