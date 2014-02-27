# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_scoremanager___import___01():
    r'''Do not import materials because any in-progress code that raises
    exceptions will prevent the entire system from starting.
    '''

    assert 'materials' not in dir(scoremanager)
