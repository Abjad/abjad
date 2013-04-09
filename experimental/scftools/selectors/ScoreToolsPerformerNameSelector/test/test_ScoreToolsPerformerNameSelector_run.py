import scftools


def test_ScoreToolsPerformerNameSelector_run_01():

    selector = scftools.selectors.ScoreToolsPerformerNameSelector()
    assert selector.run(user_input='q') is None

    selector = scftools.selectors.ScoreToolsPerformerNameSelector()
    assert selector.run(user_input='b') is None

    selector = scftools.selectors.ScoreToolsPerformerNameSelector()
    assert selector.run(user_input='studio') is None


def test_ScoreToolsPerformerNameSelector_run_02():

    selector = scftools.selectors.ScoreToolsPerformerNameSelector()
    assert selector.run(user_input='vn') == 'violinist'


def test_ScoreToolsPerformerNameSelector_run_03():

    selector = scftools.selectors.ScoreToolsPerformerNameSelector(is_ranged=True)
    assert selector.run(user_input='vn, va') == ['violinist', 'violist']
