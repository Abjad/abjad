from experimental.tools.scftools.specifiers.ParameterSpecifier import ParameterSpecifier


class ClefSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, clef_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.clef_name = clef_name

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.clef_name
