# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.RhythmMakerEditor import RhythmMakerEditor


class TaleaRhythmMakerEditor(RhythmMakerEditor):
    r'''TaleaRhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            rhythmmakertools.TaleaRhythmMaker,
            ('talea', None, 'ta', getters.get_nonzero_integers, True),
            ('talea_denominator', None, 'de', 
                getters.get_positive_integer_power_of_two, True),
            ('extra_counts_per_division', None, 'ad', getters.get_integers, False),
            ('split_divisions_by_counts', None, 'sd', getters.get_integers, False),
            )