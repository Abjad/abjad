# -*- encoding: utf-8 -*-
from abjad import *


def test_iotools_IOManager_spawn_subprocess_01():

    assert iotools.IOManager.spawn_subprocess('echo "hello world"') == 0
