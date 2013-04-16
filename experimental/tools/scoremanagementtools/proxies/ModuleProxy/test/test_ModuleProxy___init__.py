from experimental import *


def test_ModuleProxy___init___01():
    '''Init empty module proxy.
    '''

    module_proxy = scoremanagementtools.proxies.ModuleProxy()

    assert isinstance(module_proxy, scoremanagementtools.proxies.ModuleProxy)
