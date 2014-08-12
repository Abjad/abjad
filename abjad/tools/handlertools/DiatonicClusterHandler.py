# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.handlertools.Handler import Handler


class DiatonicClusterHandler(Handler):
    r'''Diatonic cluster handler.

    ..  container:: example

        ::

            >>> staff = Staff("c' d' e' f'")
            >>> handler = handlertools.DiatonicClusterHandler(
            ...     cluster_widths=[4, 6],
            ...     )
            >>> handler(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_cluster_widths',
        ) 

    ### INITIALIZER ###

    def __init__(self, cluster_widths=None):
        Handler.__init__(self)
        if cluster_widths is not None:
            cluster_widths = datastructuretools.CyclicTuple(cluster_widths)
        self._cluster_widths = cluster_widths

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls diatonic cluster handler on `expr`.

        Returns none.
        '''
        for i, note in enumerate(iterate(expr).by_class(scoretools.Note)):
            cluster_width = self.cluster_widths[i]
            start = note.written_pitch.diatonic_pitch_number
            diatonic_numbers = range(start, start + cluster_width)
            chromatic_numbers = [
                (12 * (x // 7)) +
                pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
                    x % 7]
                for x in diatonic_numbers
                ]
            chord_pitches = [pitchtools.NamedPitch(x)
                for x in chromatic_numbers]
            chord = scoretools.Chord(note)
            chord.note_heads[:] = chord_pitches
            mutate(note).replace(chord)

    ### PUBLIC PROPERTIES ###

    @property
    def cluster_widths(self):
        r'''Gets cluster widths of handler.

        Returns tuple of positive integers or none.
        '''
        return self._cluster_widths