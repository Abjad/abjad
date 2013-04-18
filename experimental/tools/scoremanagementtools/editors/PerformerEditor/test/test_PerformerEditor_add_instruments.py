from abjad import *
from experimental import *


def test_PerformerEditor_add_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup perf hornist add q')
    assert studio.ts == (12,)

    studio.run(user_input='example~score~i setup perf hornist add b q')
    assert studio.ts == (14, (8, 12))

    studio.run(user_input='example~score~i setup perf hornist add studio q')
    assert studio.ts == (14, (0, 12))

    studio.run(user_input='example~score~i setup perf hornist add score q')
    assert studio.ts == (14, (2, 12))

    studio.run(user_input='example~score~i setup perf hornist add foo q')
    assert studio.ts == (14, (10, 12))


def test_PerformerEditor_add_instruments_02():
    '''Add two instruments.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 q')
    assert editor.target == scoretools.Performer(
        instruments=[instrumenttools.Accordion(), instrumenttools.AltoFlute()])


def test_PerformerEditor_add_instruments_03():
    '''Range handling.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add 1-2 q')
    assert editor.target == scoretools.Performer(
        instruments=[instrumenttools.Accordion(), instrumenttools.AltoFlute()])
