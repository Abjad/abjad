from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier import ParameterSpecifier


class RhythmSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, rhythm_maker_package_path=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.rhythm_maker_package_path = rhythm_maker_package_path

    ### READ-ONLY PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.name or self.rhythm_maker_package_path
