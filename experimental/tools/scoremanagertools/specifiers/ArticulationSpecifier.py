# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class ArticulationSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self, 
        articulation_handler_name=None, 
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
        self.articulation_handler_name = articulation_handler_name

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.articulation_handler_name
