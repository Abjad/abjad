from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from experimental.tools.handlertools.pitch.PitchHandler import PitchHandler


class DiatonicClusterHandler(PitchHandler):

    ### INITIALIZER ###

    def __init__(self, cluster_widths):
        self.cluster_widths = sequencetools.CyclicTuple(cluster_widths)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for i, note in enumerate(iterationtools.iterate_notes_in_expr(expr)):
            cluster_width = self.cluster_widths[i]
            start = note.written_pitch.diatonic_pitch_number
            diatonic_pitch_numbers = range(start, start + cluster_width)
            chord_pitches = [pitchtools.NamedDiatonicPitch(x) for x in diatonic_pitch_numbers]
            chord = chordtools.Chord(note)
            chord[:] = []
            chord.extend(chord_pitches)
            componenttools.move_parentage_and_spanners_from_components_to_components([note], [chord])
