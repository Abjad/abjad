from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 sm q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 sm b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 sm studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))
