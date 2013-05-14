import os
from experimental import *


def test_DistributionDirectoryProxy_01():

    distribution_proxy = scoremanagertools.proxies.DistributionDirectoryProxy(
        'scoremanagertools.built_in_scores.red_example_score')

    assert distribution_proxy.filesystem_path == os.path.join(
        distribution_proxy.configuration.built_in_scores_directory_path, 
        'red_example_score', 'distribution')
    assert distribution_proxy._spaced_class_name == 'distribution directory proxy'
