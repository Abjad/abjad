from abjad import *
from abjad.tools.skiptools import Skip


def test_Skip___repr___01():
    '''Skip repr is evaluable.
    '''

    skip_1 = Skip('s8.')
    skip_2 = eval(repr(skip_1))

    assert isinstance(skip_1, Skip)
    assert isinstance(skip_2, Skip)
    assert skip_1.format == skip_2.format
    assert skip_1 is not skip_2
