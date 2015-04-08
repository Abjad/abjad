# -*- encoding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools import lilypondfiletools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import mutate


def make_lilypond_file(
    music, 
    divisions, 
    implicit_scaling=False,
    time_signatures=None,
    ):
    r'''Makes LilyPond file.

    ..  container::

        **Example 1.**

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Used in rhythm-maker docs.

    Returns LilyPond file.
    '''

    assert isinstance(music, list), repr(music)
    prototype = (selectiontools.Selection, scoretools.Tuplet)
    assert all(isinstance(x, prototype) for x in music), repr(music)
    assert isinstance(divisions, (tuple, list)), repr(divisions)
    time_signatures = time_signatures or divisions

    score = scoretools.Score()
    lilypond_file = \
        lilypondfiletools.make_floating_time_signature_lilypond_file(score)

    context = scoretools.Context(context_name='TimeSignatureContext')
    measures = scoretools.make_spacer_skip_measures(
        time_signatures,
        implicit_scaling=implicit_scaling,
        )
    context.extend(measures)
    score.append(context)

    measures = scoretools.make_spacer_skip_measures(
        time_signatures,
        implicit_scaling=implicit_scaling,
        )
    staff = scoretools.Staff(measures, context_name='RhythmicStaff')
    music = sequencetools.flatten_sequence(music)
    music_copy = copy.deepcopy(music)

    try:
        measures = mutate(staff).replace_measure_contents(music)
    except StopIteration:
        staff = scoretools.Staff(music_copy, context_name='RhythmicStaff')
        
    score.append(staff)

    return lilypond_file