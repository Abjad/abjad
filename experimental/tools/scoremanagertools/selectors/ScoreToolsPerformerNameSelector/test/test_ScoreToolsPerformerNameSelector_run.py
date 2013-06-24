from experimental import *


def test_ScoreToolsPerformerNameSelector_run_01():

    selector = scoremanagertools.selectors.ScoreToolsPerformerNameSelector()
    assert selector._run(pending_user_input='q') is None

    selector = scoremanagertools.selectors.ScoreToolsPerformerNameSelector()
    assert selector._run(pending_user_input='b') is None

    selector = scoremanagertools.selectors.ScoreToolsPerformerNameSelector()
    assert selector._run(pending_user_input='home') is None


def test_ScoreToolsPerformerNameSelector_run_02():

    selector = scoremanagertools.selectors.ScoreToolsPerformerNameSelector()
    assert selector._run(pending_user_input='vn') == 'violinist'


def test_ScoreToolsPerformerNameSelector_run_03():

    selector = scoremanagertools.selectors.ScoreToolsPerformerNameSelector(is_ranged=True)
    assert selector._run(pending_user_input='vn, va') == ['violinist', 'violist']
