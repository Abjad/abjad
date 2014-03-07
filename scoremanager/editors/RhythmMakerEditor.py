# -*- encoding: utf-8 -*-
from scoremanager.editors.Editor import Editor


class RhythmMakerEditor(Editor):
    r'''RhythmMaker editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(Editor.target_summary_lines.fget(self))
        return result
