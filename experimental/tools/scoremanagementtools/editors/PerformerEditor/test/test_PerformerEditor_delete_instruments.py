from abjad import *
from experimental import *


def test_PerformerEditor_delete_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup perf hornist rm q')
    assert studio.ts == (11,)

    studio.run(user_input='example~score~i setup perf hornist rm b q')
    assert studio.ts == (13, (8, 11))

    studio.run(user_input='example~score~i setup perf hornist rm studio q')
    assert studio.ts == (13, (0, 11))

    studio.run(user_input='example~score~i setup perf hornist rm score q')
    assert studio.ts == (13, (2, 11))

    studio.run(user_input='example~score~i setup perf hornist rm foo q')
    transcript = studio.transcript
    assert studio.ts == (13,)


def test_PerformerEditor_delete_instruments_02():
    '''Add two instruments. Delete one.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add flute add acc rm flute q')
    assert editor.target == scoretools.Performer(instruments=[instrumenttools.Accordion()])


def test_PerformerEditor_delete_instruments_03():
    '''Numeric range handling.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='add 1-3 rm 1,3 q')
    assert editor.target == scoretools.Performer(instruments=[instrumenttools.AltoFlute()])
