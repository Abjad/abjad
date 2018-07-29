import abjad


def test_IOManager_spawn_subprocess_01():

    assert abjad.IOManager.spawn_subprocess('echo "hello world"') == 0
