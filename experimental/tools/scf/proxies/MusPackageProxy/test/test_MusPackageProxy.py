import scf


def test_MusPackageProxy_01():

    mus_proxy = scf.proxies.MusPackageProxy('manos')

    assert mus_proxy.path_name == '/Users/trevorbaca/Documents/scores/manos/mus'
    assert mus_proxy.short_name == 'mus'
    assert mus_proxy.importable_name == 'manos.mus'
