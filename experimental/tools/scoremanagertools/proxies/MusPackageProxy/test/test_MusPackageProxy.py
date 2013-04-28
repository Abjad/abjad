import os
from experimental import *


def test_MusPackageProxy_01():

    mus_proxy = scoremanagertools.proxies.MusPackageProxy('example_score_1')

    assert mus_proxy.directory_path == os.path.join(
        mus_proxy.configuration.scores_directory_path, 'example_score_1', 'mus')
    assert mus_proxy.name == 'mus'
    assert mus_proxy.package_path == 'example_score_1.mus'
