# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_delete_performers_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    string = 'red~example~score setup instrumentation rm q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (9,)

    string = 'red~example~score setup instrumentation rm b q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11, (6, 9))

    string = 'red~example~score setup instrumentation rm h q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11, (0, 9))

    string = 'red~example~score setup instrumentation rm s q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11, (2, 9))

    string = 'red~example~score setup instrumentation rm foo q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11, (6, 9))


def test_InstrumentationEditor_delete_performers_02():
    r'''Add three performers. Delete two.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentationEditor(session=session)
    string = 'add acc default add bass default add bassoon default rm 3 rm 2 q'
    editor._run(pending_user_input=string)
    assert editor.target == instrumenttools.InstrumentationSpecifier(
        [
            instrumenttools.Performer(
                'accordionist', 
                instruments=[instrumenttools.Accordion()],
                ),
            ]
        )


def test_InstrumentationEditor_delete_performers_03():
    r'''Range handling.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentationEditor(session=session)
    editor._run(pending_user_input='add 1-3 default default default rm 3-2 q')
    assert editor.target == instrumenttools.InstrumentationSpecifier(
        [
            instrumenttools.Performer(
                'accordionist', 
                instruments=[instrumenttools.Accordion()],
                )
            ]
        )
