from experimental import *


def test_PackageProxy_manage_tags_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score tags q')
    assert studio.ts == (6,)

    studio.run(user_input='example~score tags b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='example~score tags studio q')
    assert studio.ts == (8, (0, 6))

    studio.run(user_input='example~score tags score q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='example~score tags foo q')
    assert studio.ts == (8, (4, 6))
