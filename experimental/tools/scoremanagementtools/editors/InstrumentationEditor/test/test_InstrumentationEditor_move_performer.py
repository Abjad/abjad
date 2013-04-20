from abjad import *
from experimental import *


def test_InstrumentationEditor_move_performer_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='example~score~i setup perf move q')
    assert score_manager.ts == (9,)

    score_manager.run(user_input='example~score~i setup perf move b q')
    assert score_manager.ts == (11, (6, 9))

    score_manager.run(user_input='example~score~i setup perf move home q')
    assert score_manager.ts == (11, (0, 9))

    score_manager.run(user_input='example~score~i setup perf move score q')
    assert score_manager.ts == (11, (2, 9))

    score_manager.run(user_input='example~score~i setup perf move foo q')
    assert score_manager.ts == (11,)


def test_InstrumentationEditor_move_performer_02():
    '''Add three performers. Make two moves.
    '''

    editor = scoremanagementtools.editors.InstrumentationEditor()
    editor.run(user_input=
        'add accordionist default add bassist default add bassoonist bassoon move 1 2 move 2 3 q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='bassist', instruments=[instrumenttools.Contrabass()]),
        scoretools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()])])
