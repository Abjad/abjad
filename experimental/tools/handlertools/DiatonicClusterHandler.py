# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import datastructuretools
from abjad.tools import iterationtools
from abjad.tools import mutationtools
from abjad.tools import pitchtools
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
        self.cluster_widths = datastructuretools.CyclicTuple(cluster_widths)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for i, note in enumerate(iterationtools.iterate_notes_in_expr(expr)):
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
            chord[:] = []
            chord.extend(chord_pitches)
            mutationtools.mutate(note).replace(chord)
