from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import marktools
from abjad.tools import notetools
from abjad.tools import tietools


def edit_viola_voice(score, durated_reservoir):

    voice = score['Viola Voice']
    descents = durated_reservoir['Viola']

    for leaf in descents[-1]:
        marktools.Articulation('accent')(leaf)
        marktools.Articulation('tenuto')(leaf)
    copied_descent = componenttools.copy_components_and_remove_spanners(descents[-1])
    for leaf in copied_descent:
        if leaf.written_duration == durationtools.Duration(4, 4):
            leaf.written_duration = durationtools.Duration(8, 4)
        else:
            leaf.written_duration = durationtools.Duration(4, 4)
    voice.extend(copied_descent)

    bridge = notetools.Note('e1')
    marktools.Articulation('tenuto')(bridge)
    marktools.Articulation('accent')(bridge)
    voice.append(bridge)

    final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    final_sustain_notes = notetools.make_notes(['e'], final_sustain_rhythm)
    marktools.Articulation('accent')(final_sustain_notes[0])
    marktools.Articulation('tenuto')(final_sustain_notes[0])
    voice.extend(final_sustain_notes)
    tietools.TieSpanner(final_sustain_notes)
    voice.extend('r4 r2.')

