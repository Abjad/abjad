from experimental import *


def test_PerformerEditor_run_01():
    '''Quit, back, studio and junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers hornist q')
    assert studio.ts == (10,)

    studio.run(user_input='example~score~i setup performers hornist b q')
    assert studio.ts == (12, (6, 10))

    studio.run(user_input='example~score~i setup performers hornist studio q')
    assert studio.ts == (12, (0, 10))

    studio.run(user_input='example~score~i setup performers hornist foo q')
    assert studio.ts == (12, (8, 10))
