# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_add_performers_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation add q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (10,)

    string = 'red~example~score setup instrumentation add b q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (12, (6, 10))

    string = 'red~example~score setup instrumentation add h q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (12, (0, 10))

    string = 'red~example~score setup instrumentation add score q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (12, (2, 10))

    string = 'red~example~score setup instrumentation add foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    r'''Add three performers.
    '''

    editor = scoremanager.editors.InstrumentationEditor()
    string = 'add accordionist default add bassoonist default'
    string += ' add cellist default q'
    editor._run(pending_user_input=string)
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='accordionist', 
            instruments=[instrumenttools.Accordion()],
            ),
        instrumenttools.Performer(
            name='bassoonist', 
            instruments=[instrumenttools.Bassoon()],
            ),
        instrumenttools.Performer(
            name='cellist', 
            instruments=[instrumenttools.Cello()],
            )])


def test_InstrumentationEditor_add_performers_03():
    r'''Range handling.
    '''

    editor = scoremanager.editors.InstrumentationEditor()
    editor._run(pending_user_input='add 1-3 default default default q')
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='accordionist', 
            instruments=[instrumenttools.Accordion()]),
        instrumenttools.Performer(
            name='alto', 
            instruments=[instrumenttools.AltoVoice()]),
        instrumenttools.Performer(
            name='baritone', 
            instruments=[instrumenttools.BaritoneVoice()]),
            ])
