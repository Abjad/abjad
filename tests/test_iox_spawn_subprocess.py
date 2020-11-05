import abjad


def test_iox_spawn_subprocess_01():

    assert abjad.iox.spawn_subprocess('echo "hello world"') == 0
