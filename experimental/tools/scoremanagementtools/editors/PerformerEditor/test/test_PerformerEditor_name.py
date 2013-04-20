from abjad import *
from experimental import *


def test_PerformerEditor_name_01():
    '''Quit, back and studio all work.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist name q')
    assert score_manager.ts == (11,)

    score_manager.run(user_input='example~score~i setup performers hornist name b q')
    assert score_manager.ts == (13, (8, 11))

    score_manager.run(user_input='example~score~i setup performers hornist name home q')
    assert score_manager.ts == (13, (0, 11))


def test_PerformerEditor_name_02():
    '''String input only.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist name -99 q')
    assert score_manager.ts == (13,)


def test_PerformerEditor_name_03():
    '''Create, name and rename performer.
    '''

    editor = scoremanagementtools.editors.PerformerEditor()
    editor.run(user_input='name foo name bar q')
    assert editor.target == scoretools.Performer(name='bar')
