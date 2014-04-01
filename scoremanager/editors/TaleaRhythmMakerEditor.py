# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class TaleaRhythmMakerEditor(Editor):
    r'''TaleaRhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _get_target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(Editor._target_summary_lines.fget(self))
        return result