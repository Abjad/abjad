import scftools


def test_ScorePackageWrangler_run_01():
    '''Create score package. Remove score package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('testscore')

    try:
        studio.run(user_input=
            'new Test~score testscore 2012 '
            'q'
            )
        assert studio.package_exists('testscore')
        spp = scftools.proxies.ScorePackageProxy('testscore')
        assert spp.annotated_title == 'Test score (2012)'
        assert spp.composer is None
        assert spp.instrumentation is None
    finally:
        studio.run(user_input='test removescore clobberscore remove default q')
        assert not studio.package_exists('testscore')
