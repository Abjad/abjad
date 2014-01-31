# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_datastructuretools_StatalServerCursor___call___01():
    r'''Invalid levels raise an exception.
    '''
    
    sequence = [(0, 1), (2, 3), (4, 5), (6, 7)]
    server = datastructuretools.StatalServer(sequence)
    cursor = server()

    statement = 'cursor(level=-99)'
    assert pytest.raises(Exception, statement)
