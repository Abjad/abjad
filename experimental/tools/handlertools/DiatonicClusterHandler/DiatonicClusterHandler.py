# -*- encoding: utf-8 -*-
from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from experimental.tools.handlertools.PitchHandler import PitchHandler


class DiatonicClusterHandler(PitchHandler):
    r'''Diatonic cluster handler:

    ::

        >>> staff = Staff("c' d' e' f'")
        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> diatonic_cluster_handler = handlertools.DiatonicClusterHandler(
        ...     [4, 6])
        >>> diatonic_cluster_handler(staff)

    ::

        >>> f(staff) 
        \new Staff {
            <c' d' e' f'>4
            <d' e' f' g' a' b'>4
            <e' f' g' a'>4
            <f' g' a' b' c'' d''>4
        }

    '''

    ### INITIALIZER ###

    def __init__(self, cluster_widths):
        self.cluster_widths = sequencetools.CyclicTuple(cluster_widths)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for i, note in enumerate(iterationtools.iterate_notes_in_expr(expr)):
            cluster_width = self.cluster_widths[i]
            start = note.written_pitch.diatonic_pitch_number
            diatonic_numbers = range(start, start + cluster_width)
            chromatic_numbers = [
                pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(x)
                for x in diatonic_numbers 
                ] 
            chord_pitches = [pitchtools.NamedChromaticPitch(x) 
                for x in chromatic_numbers]
            chord = chordtools.Chord(note)
            chord[:] = []
            chord.extend(chord_pitches)
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [note], [chord])

