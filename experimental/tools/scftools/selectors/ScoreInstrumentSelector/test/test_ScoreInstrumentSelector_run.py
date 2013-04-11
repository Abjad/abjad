from abjad import *
from experimental import *


def test_ScoreInstrumentSelector_run_01():

    selector = scftools.selectors.ScoreInstrumentSelector()
    selector.session.current_score_package_short_name = 'example_score_1'

    assert selector.run(user_input='vio') == instrumenttools.Violin()
    assert selector.run(user_input='oth') == 'other'
