# -*- encoding: utf-8 -*-
from scoremanager.editors.Editor import Editor


class RhythmMakerEditor(Editor):
    r'''RhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(Editor._target_summary_lines.fget(self))
        return result