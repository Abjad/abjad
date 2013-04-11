from experimental.tools.scftools.editors.InteractiveEditor import InteractiveEditor


class ParameterSpecifierEditor(InteractiveEditor):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target:
            return self.target.one_line_menuing_summary
