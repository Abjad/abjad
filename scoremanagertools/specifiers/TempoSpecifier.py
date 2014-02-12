# -*- encoding: utf-8 -*-
from scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class TempoSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self,
        description=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier
