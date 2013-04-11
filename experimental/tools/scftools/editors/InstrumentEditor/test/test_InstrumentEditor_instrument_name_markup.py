from abjad import *
from experimental import *


def test_InstrumentEditor_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 im q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 im b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 im studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))
