# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondfiletools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import mutate


def make_example_lilypond_file(music, divisions):
    r'''Makes example LilyPond file.

    ..  container::

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_example_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Used in rhythm-maker docs.

    Returns LilyPond file.
    '''

    score = scoretools.Score()
    lilypond_file = \
        lilypondfiletools.make_floating_time_signature_lilypond_file(score)

    context = scoretools.Context(context_name='TimeSignatureContext')
    measures = scoretools.make_spacer_skip_measures(divisions)
    context.extend(measures)
    score.append(context)

    measures = scoretools.make_spacer_skip_measures(divisions)
    staff = scoretools.RhythmicStaff(measures)
    music = sequencetools.flatten_sequence(music)
    measures = mutate(staff).replace_measure_contents(music)
    score.append(staff)

    return lilypond_file
