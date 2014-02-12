# -*- encoding: utf-8 -*-
from scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class RhythmMakerEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(InteractiveEditor.target_summary_lines.fget(self))
        return result
