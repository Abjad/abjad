import os
from experimental import *


def test_MusPackageProxy_01():

    mus_proxy = scoremanagertools.proxies.MusPackageProxy('example_score_1')

    assert mus_proxy.path_name == os.path.join(
        mus_proxy.configuration.SCORES_DIRECTORY_PATH, 'example_score_1', 'mus')
    assert mus_proxy.short_name == 'mus'
    assert mus_proxy.importable_name == 'example_score_1.mus'
