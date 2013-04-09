from abjad import *
import scftools


def test_PerformerEditor_run_01():
    '''Quit, back, studio and junk all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers 1 q')
    assert studio.ts == (10, (1, 7))

    studio.run(user_input='1 setup performers 1 b q')
    assert studio.ts == (12, (1, 7), (6, 10))

    studio.run(user_input='1 setup performers 1 studio q')
    assert studio.ts == (12, (0, 10), (1, 7))

    studio.run(user_input='1 setup performers 1 foo q')
    assert studio.ts == (12, (1, 7), (8, 10))
