import scf


def test_ModuleProxy___init___01():
    '''Init empty module proxy.
    '''

    module_proxy = scf.proxies.ModuleProxy()

    assert isinstance(module_proxy, scf.proxies.ModuleProxy)
