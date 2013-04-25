import os
from experimental import *


def test_DistDirectoryProxy_01():

    dist_proxy = scoremanagertools.proxies.DistDirectoryProxy('example_score_1')

    assert dist_proxy.path == os.path.join(
        dist_proxy.configuration.SCORES_DIRECTORY_PATH, 'example_score_1', 'dist')
    assert dist_proxy.source_file_name == \
        os.path.join(
            dist_proxy.configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH,
            'proxies', 'DistDirectoryProxy', 'DistDirectoryProxy.py')
    assert dist_proxy._spaced_class_name == 'dist directory proxy'
