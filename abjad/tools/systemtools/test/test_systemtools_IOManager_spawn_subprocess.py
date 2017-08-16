import abjad
from abjad.tools import systemtools


def test_systemtools_IOManager_spawn_subprocess_01():

    assert systemtools.IOManager.spawn_subprocess('echo "hello world"') == 0
