import os
from experimental import *


def test_EtcDirectoryProxy_01():

    etc_proxy = scoremanagementtools.proxies.EtcDirectoryProxy('example_score_1')

    assert etc_proxy.path_name == os.path.join(os.environ.get('SCORES'), 'example_score_1', 'etc')
    assert etc_proxy.source_file_name == \
        os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'proxies', 'EtcDirectoryProxy', 'EtcDirectoryProxy.py')
    assert etc_proxy._spaced_class_name == 'etc directory proxy'
