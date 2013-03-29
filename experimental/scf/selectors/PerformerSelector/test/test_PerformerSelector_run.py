from abjad.tools import instrumenttools
from abjad.tools import scoretools
import scf


def test_PerformerSelector_run_01():

    selector = scf.selectors.PerformerSelector()
    selector.session._current_score_package_short_name = 'betoerung'
    result = selector.run(user_input='1')

    assert result == scoretools.Performer(name='hornist', instruments=[instrumenttools.FrenchHorn()])
