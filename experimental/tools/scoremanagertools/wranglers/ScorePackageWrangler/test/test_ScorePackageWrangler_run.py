from experimental import *


def test_ScorePackageWrangler_run_01():
    '''Create score package. Remove score package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.package_exists('testscore')

    try:
        score_manager.run(user_input=
            'new Test~score testscore 2012 '
            'q'
            )
        assert score_manager.package_exists('testscore')
        spp = scoremanagertools.proxies.ScorePackageProxy('testscore')
        assert spp.annotated_title == 'Test score (2012)'
        assert spp.composer is None
        assert spp.instrumentation is None
    finally:
        score_manager.run(user_input='test removescore clobberscore remove default q')
        assert not score_manager.package_exists('testscore')
