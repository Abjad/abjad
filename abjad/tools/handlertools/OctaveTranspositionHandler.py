# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.handlertools.Handler import Handler


class OctaveTranspositionHandler(Handler):
    r'''Octave transposition handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_octave_transposition_mapping',
        )
    
    ### INITIALIZER ###

    def __init__(self, octave_transposition_mapping=None):
        if octave_transposition_mapping is not None:
            octave_transposition_mapping = \
                pitchtools.Registration(
                    octave_transposition_mapping)
        self._octave_transposition_mapping = octave_transposition_mapping

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            if isinstance(leaf, Note):
                n = leaf.pitch.pitch_number
                n = pitchtools.transpose_pitch_number_by_octave_transposition_mapping(
                    n, self.octave_transposition_mapping)
                leaf.pitch = n
            elif isinstance(leaf, Chord):
                nn = [nh.pitch.pitch_number for nh in leaf]
                nn = [pitchtools.transpose_pitch_number_by_octave_transposition_mapping(
                    n, self.octave_transposition_mapping) for n in nn]
                leaf.pitches = nn

    ### PUBLIC PROPERTIES ###

    @property
    def octave_transposition_mapping(self):
        r'''Gets octave transposition mapping of handler.

        Returns octave transposition mapping or none.
        '''
        return self._octave_transposition_mapping