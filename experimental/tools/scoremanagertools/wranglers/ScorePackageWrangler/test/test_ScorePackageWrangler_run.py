from experimental import *
import py


def test_ScorePackageWrangler_run_01():
    '''Create score package. Remove score package.
    '''
    py.test.skip('unskip after deciding about cache.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not packagesystemtools.exists('testscore')

    try:
        score_manager._run(user_input=
            'new Test~score testscore 2012 '
            'q'
            )
        assert packagesystemtools.exists('testscore')
        spp = scoremanagertools.proxies.ScorePackageProxy('testscore')
        assert spp.annotated_title == 'Test score (2012)'
        assert spp.composer is None
        assert spp.instrumentation is None
    finally:
        score_manager._run(user_input='test removescore clobberscore remove default q')
        assert not packagesystemtools.exists('testscore')
