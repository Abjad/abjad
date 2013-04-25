from experimental.tools.scoremanagertools.editors.InteractiveEditor import InteractiveEditor


class RhythmMakerEditor(InteractiveEditor):

    ### READ-ONLY PROPERTIES ###

    @property
    def target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target._class_name)
            result.append('')
            result.extend(InteractiveEditor.target_summary_lines.fget(self))
        return result
