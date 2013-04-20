from experimental import *


def test_PackageProxy_manage_tags_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i tags q')
    assert studio.ts == (6,)

    studio.run(user_input='example~score~i tags b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='example~score~i tags studio q')
    assert studio.ts == (8, (0, 6))

    studio.run(user_input='example~score~i tags score q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='example~score~i tags foo q')
    assert studio.ts == (8, (4, 6))
