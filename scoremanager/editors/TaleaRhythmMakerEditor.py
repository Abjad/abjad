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

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            rhythmmakertools.TaleaRhythmMaker,
            (
                'talea', 
                None, 
                'ta', 
                getters.get_nonzero_integers, 
                True,
                ),
            (
                'talea_denominator', 
                None, 
                'de', 
                getters.get_positive_integer_power_of_two, 
                True,
                ),
            (
                'extra_counts_per_division', 
                None, 
                'ad', 
                getters.get_integers, 
                False,
                ),
            (
                'split_divisions_by_counts', 
                None, 
                'sd', 
                getters.get_integers, 
                False,
                ),
            )

    ### PRIVATE METHODS ###

    def _get_target_summary_lines(self):
        result = []
        if self.target:
            result.append(self.target.__class__.__name__)
            result.append('')
            result.extend(Editor._target_summary_lines.fget(self))
        return result