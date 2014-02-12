# -*- encoding: utf-8 -*-
from scoremanager.specifiers.ParameterSpecifier import ParameterSpecifier


class PitchClassSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self,
        description=None,
        custom_identifier=None,
        pitch_class_reservoir=None,
        pitch_class_reservoir_helper=None,
        pitch_class_transform=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.pitch_class_reservoir = pitch_class_reservoir
        self.pitch_class_reservoir_helper = pitch_class_reservoir_helper
        self.pitch_class_transform = pitch_class_transform

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or \
            self.pitch_class_reservoir._one_line_menuing_summary
