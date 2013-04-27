import os
from experimental import *


def test_MusPackageProxy_01():

    mus_proxy = scoremanagertools.proxies.MusPackageProxy('example_score_1')

    assert mus_proxy.path == os.path.join(
        mus_proxy.configuration.SCORES_DIRECTORY_PATH, 'example_score_1', 'mus')
    assert mus_proxy.name == 'mus'
    assert mus_proxy.package_path == 'example_score_1.mus'
