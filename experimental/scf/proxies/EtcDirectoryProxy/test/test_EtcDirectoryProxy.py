import os
import scf


def test_EtcDirectoryProxy_01():

    etc_proxy = scf.proxies.EtcDirectoryProxy('manos')

    assert etc_proxy.path_name == '/Users/trevorbaca/Documents/scores/manos/etc'
    assert etc_proxy.is_versioned
    assert etc_proxy.source_file_name == \
        os.path.join(os.environ.get('SCFPATH'), 'proxies', 'EtcDirectoryProxy', 'EtcDirectoryProxy.py')
    assert etc_proxy.spaced_class_name == 'etc directory proxy'
