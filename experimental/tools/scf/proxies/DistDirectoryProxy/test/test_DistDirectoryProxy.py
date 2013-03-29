import scf


def test_DistDirectoryProxy_01():

    dist_proxy = scf.proxies.DistDirectoryProxy('manos')

    assert dist_proxy.path_name == '/Users/trevorbaca/Documents/scores/manos/dist'
    assert dist_proxy.is_versioned
    assert dist_proxy.source_file_name == \
        '/Users/trevorbaca/Documents/baca/scf/proxies/DistDirectoryProxy/DistDirectoryProxy.py'
    assert dist_proxy.spaced_class_name == 'dist directory proxy'
