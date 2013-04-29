from abjad import *
from experimental import *


def test_PerformerEditor_add_instruments_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup perf hornist add q')
    assert score_manager.transcript_signature == (12,)

    score_manager.run(user_input='example~score~i setup perf hornist add b q')
    assert score_manager.transcript_signature == (14, (8, 12))

    score_manager.run(user_input='example~score~i setup perf hornist add home q')
    assert score_manager.transcript_signature == (14, (0, 12))

    score_manager.run(user_input='example~score~i setup perf hornist add score q')
    assert score_manager.transcript_signature == (14, (2, 12))

    score_manager.run(user_input='example~score~i setup perf hornist add foo q')
    assert score_manager.transcript_signature == (14, (10, 12))


def test_PerformerEditor_add_instruments_02():
    '''Add two instruments.
    '''

    editor = scoremanagertools.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 q')
    assert editor.target == scoretools.Performer(
        instruments=[instrumenttools.Accordion(), instrumenttools.AltoFlute()])


def test_PerformerEditor_add_instruments_03():
    '''Range handling.
    '''

    editor = scoremanagertools.editors.PerformerEditor()
    editor.run(user_input='add 1-2 q')
    assert editor.target == scoretools.Performer(
        instruments=[instrumenttools.Accordion(), instrumenttools.AltoFlute()])
