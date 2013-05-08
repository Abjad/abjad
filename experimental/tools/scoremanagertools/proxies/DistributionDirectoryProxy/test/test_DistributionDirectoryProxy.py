import os
from experimental import *


def test_DistributionDirectoryProxy_01():

    distribution_proxy = scoremanagertools.proxies.DistributionDirectoryProxy('example_score_1')

    assert distribution_proxy.filesystem_path == os.path.join(
        distribution_proxy.configuration.user_scores_directory_path, 'example_score_1', 'distribution')
    assert distribution_proxy._spaced_class_name == 'distribution directory proxy'
