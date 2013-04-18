from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers hornist horn sm q')
    assert studio.ts == (13,)

    studio.run(user_input='example~score~i setup performers hornist horn sm b q')
    assert studio.ts == (15, (10, 13))

    studio.run(user_input='example~score~i setup performers hornist horn sm studio q')
    assert studio.ts == (15, (0, 13))
