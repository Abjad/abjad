import os
import scf


def test_ExgDirectoryProxy_01():

    exg_proxy = scf.proxies.ExgDirectoryProxy('manos')

    assert exg_proxy.path_name == '/Users/trevorbaca/Documents/scores/manos/exg'
    assert exg_proxy.is_versioned
    assert exg_proxy.source_file_name == \
        os.path.join(os.environ.get('SCFPATH'), 'proxies', 'ExgDirectoryProxy', 'ExgDirectoryProxy.py')
    assert exg_proxy.spaced_class_name == 'exg directory proxy'
