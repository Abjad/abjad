from experimental import *


def test_Session_command_repetition_01():

    studio = scftools.studio.Studio()
    studio.run(user_input='next . . . q')
    assert studio.session.command_history == ['next', '.', '.', '.', 'q']
    assert studio.ts == (10, (1, 3, 5, 7))


def test_Session_command_repetition_02():

    studio = scftools.studio.Studio()
    studio.run(user_input='{{next perf}} q')
    assert studio.session.command_history == ['next perf', 'q']
    assert studio.ts == (4,)

    studio.run(user_input='{{next perf}} . q')
    assert studio.session.command_history == ['next perf', '.', 'q']
    assert studio.ts == (6, (1, 3))

    studio.run(user_input='{{next perf}} . . q')
    assert studio.session.command_history == ['next perf', '.', '.', 'q']
    assert studio.ts == (8, (1, 3, 5))
