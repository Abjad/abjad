from abjad import *
from experimental import *


def test_InstrumentEditor_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn q')
    assert studio.ts == (12,)

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn b q')
    assert studio.ts == (14, (8, 12))

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn studio q')
    assert studio.ts == (14, (0, 12))

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn score q')
    assert studio.ts == (14, (2, 12))

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn foo q')
    assert studio.ts == (14, (10, 12))
