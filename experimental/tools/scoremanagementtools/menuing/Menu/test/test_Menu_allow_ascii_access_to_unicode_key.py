from experimental import *


def test_Menu_allow_ascii_access_to_unicode_key_01():

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='Étude q')
    assert studio.ts == (4,)

    studio.run(user_input='étude q')
    assert studio.ts == (4,)

    studio.run(user_input='Etude q')
    assert studio.ts == (4,)

    studio.run(user_input='etude q')
    assert studio.ts == (4,)
