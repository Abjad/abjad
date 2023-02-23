import abjad


def test_io_spawn_subprocess_01():
    assert abjad.io.spawn_subprocess('echo "hello world"') == 0
