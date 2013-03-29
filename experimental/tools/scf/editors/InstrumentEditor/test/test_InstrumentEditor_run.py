from abjad import *
import scf


def test_InstrumentEditor_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 q')
    assert studio.ts == (12, (1, 7, 9))

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 b q')
    assert studio.ts == (14, (1, 7, 9), (8, 12))

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 studio q')
    assert studio.ts == (14, (0, 12), (1, 7, 9))

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 score q')
    assert studio.ts == (14, (1, 7, 9), (2, 12))

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 foo q')
    assert studio.ts == (14, (1, 7, 9), (10, 12))
