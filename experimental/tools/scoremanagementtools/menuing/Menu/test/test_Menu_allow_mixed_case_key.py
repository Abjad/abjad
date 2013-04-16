from experimental import *


def test_Menu_allow_mixed_case_key_01():
    '''Allow mixed case 'stu' key.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input="L'arch stu q")
    assert studio.ts == (6, (0, 4))

    studio.run(user_input="L'arch STU q")
    assert studio.ts == (6, (0, 4))

    studio.run(user_input="L'arch sTu q")
    assert studio.ts == (6, (0, 4))

    studio.run(user_input="L'arch sTU q")
    assert studio.ts == (6, (0, 4))
