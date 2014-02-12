# -*- encoding: utf-8 -*-
from scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class ClefSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self, 
        description=None, 
        clef_name=None, 
        custom_identifier=None, 
        source=None,
        ):
        ParameterSpecifier.__init__(
            self, 
            description=description, 
            custom_identifier=custom_identifier, 
            source=source,
            )
        self.clef_name = clef_name

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.clef_name
