from experimental import *


def test_InstrumentationEditor_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup perf q')
    assert studio.ts == (8,)

    studio.run(user_input='1 setup perf b q')
    assert studio.ts == (10, (4, 8))

    studio.run(user_input='1 setup perf studio q')
    assert studio.ts == (10, (0, 8))

    studio.run(user_input='1 setup perf score q')
    assert studio.ts == (10, (2, 8))

    studio.run(user_input='1 setup perf foo q')
    assert studio.ts == (10, (6, 8))
