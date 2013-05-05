import os
from experimental import *


def test_DistributionDirectoryProxy_01():

    dist_proxy = scoremanagertools.proxies.DistributionDirectoryProxy('example_score_1')

    assert dist_proxy.directory_path == os.path.join(
        dist_proxy.configuration.scores_directory_path, 'example_score_1', 'distribution')
    assert dist_proxy._spaced_class_name == 'distribution directory proxy'
