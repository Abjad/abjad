# -*- encoding: utf-8 -*-
from abjad import *


def test_iotools_spawn_subprocess_01():

    assert iotools.spawn_subprocess('echo "hello world"') == 0
