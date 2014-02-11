# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class ParameterSpecifierEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target:
            return self.target._one_line_menuing_summary
