# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentationEditor_add_performers_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add q')
    assert score_manager.session.io_transcript.signature == (10,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add b q')
    assert score_manager.session.io_transcript.signature == (12, (6, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add home q')
    assert score_manager.session.io_transcript.signature == (12, (0, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add score q')
    assert score_manager.session.io_transcript.signature == (12, (2, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add foo q')
    assert score_manager.session.io_transcript.signature == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    r'''Add three performers.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor._run(pending_user_input='add accordionist default add bassoonist default add cellist default q')
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()]),
        instrumenttools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        instrumenttools.Performer(name='cellist', instruments=[instrumenttools.Cello()])])


def test_InstrumentationEditor_add_performers_03():
    r'''Range handling.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor._run(pending_user_input='add 1-3 default default default q')
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='accordionist', instruments=[instrumenttools.Accordion()]),
        instrumenttools.Performer(
            name='alto', instruments=[instrumenttools.AltoVoice()]),
        instrumenttools.Performer(
            name='baritone', instruments=[instrumenttools.BaritoneVoice()])])
