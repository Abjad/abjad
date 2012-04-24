from abjad import *


def test_iotools_spawn_subprocess_01():

    assert iotools.spawn_subprocess('echo "hello world"') is None
