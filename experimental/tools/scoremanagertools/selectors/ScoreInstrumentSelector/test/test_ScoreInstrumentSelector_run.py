from abjad import *
from experimental import *


def test_ScoreInstrumentSelector_run_01():

    selector = scoremanagertools.selectors.ScoreInstrumentSelector()
    selector.session.underscore_delimited_current_score_name = 'example_score_1'

    assert selector.run(user_input='vio') == instrumenttools.Violin()
    assert selector.run(user_input='oth') == 'other'
