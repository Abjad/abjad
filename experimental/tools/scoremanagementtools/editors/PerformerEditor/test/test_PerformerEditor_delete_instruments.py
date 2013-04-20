from abjad import *
from experimental import *


def test_PerformerEditor_delete_instruments_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='example~score~i setup perf hornist rm q')
    assert score_manager.ts == (11,)

    score_manager.run(user_input='example~score~i setup perf hornist rm b q')
    assert score_manager.ts == (13, (8, 11))

    score_manager.run(user_input='example~score~i setup perf hornist rm home q')
    assert score_manager.ts == (13, (0, 11))

    score_manager.run(user_input='example~score~i setup perf hornist rm score q')
    assert score_manager.ts == (13, (2, 11))

    score_manager.run(user_input='example~score~i setup perf hornist rm foo q')
    transcript = score_manager.transcript
    assert score_manager.ts == (13,)


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
