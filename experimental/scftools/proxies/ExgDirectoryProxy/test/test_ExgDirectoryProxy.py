import os
import scftools


def test_ExgDirectoryProxy_01():

    exg_proxy = scftools.proxies.ExgDirectoryProxy('example_score_1')

    assert exg_proxy.path_name == os.path.join(os.environ.get('SCORES'), 'example_score_1', 'exg')
    assert exg_proxy.source_file_name == \
        os.path.join(os.environ.get('SCFPATH'), 'proxies', 'ExgDirectoryProxy', 'ExgDirectoryProxy.py')
    assert exg_proxy.spaced_class_name == 'exg directory proxy'
