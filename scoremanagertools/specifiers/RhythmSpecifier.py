# -*- encoding: utf-8 -*-
from scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class RhythmSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self,
        description=None,
        rhythm_maker_package_path=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.rhythm_maker_package_path = rhythm_maker_package_path

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.rhythm_maker_package_path
