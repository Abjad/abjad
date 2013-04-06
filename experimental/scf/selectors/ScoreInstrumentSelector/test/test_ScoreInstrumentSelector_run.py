from abjad import *
import scf


def test_ScoreInstrumentSelector_run_01():

    selector = scf.selectors.ScoreInstrumentSelector()
    selector.session.current_score_package_short_name = 'example_score_1'

    assert selector.run(user_input='vio') == instrumenttools.Violin()
    assert selector.run(user_input='oth') == 'other'
