import os
import scftools


def test_MusPackageProxy_01():

    mus_proxy = scftools.proxies.MusPackageProxy('example_score_1')

    assert mus_proxy.path_name == os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus')
    assert mus_proxy.short_name == 'mus'
    assert mus_proxy.importable_name == 'example_score_1.mus'
