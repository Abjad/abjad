# -*- coding: utf-8 -*-
import copy
from abjad.tools import lilypondfiletools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import mutate


def make_lilypond_file(
    selections,
    divisions,
    implicit_scaling=None,
    pitched_staff=None,
    time_signatures=None,
    ):
    r'''Makes LilyPond file.

    ..  container::

        **Example 1.**

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(exponent=1)
            >>> divisions = [(3, 4), (4, 8), (1, 4)]
            >>> selections = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Used in rhythm-maker docs.

    Returns LilyPond file.
    '''
    assert isinstance(selections, list), repr(selections)
    prototype = selectiontools.Selection
    assert all(isinstance(_, prototype) for _ in selections), repr(selections)
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
    if pitched_staff:
        staff = scoretools.Staff(measures)
    else:
        staff = scoretools.Staff(measures, context_name='RhythmicStaff')
    selections = sequencetools.flatten_sequence(selections)
    selections_ = copy.deepcopy(selections)
    try:
        measures = mutate(staff).replace_measure_contents(selections)
    except StopIteration:
        if pitched_staff:
            staff = scoretools.Staff(selections_)
        else:
            staff = scoretools.Staff(selections_, context_name='RhythmicStaff')
    score.append(staff)
    return lilypond_file
