# -*- encoding: utf-8 -*-
from experimental import *


def test_ModuleProxy___init___01():
    r'''Init empty module proxy.
    '''

    module_proxy = scoremanagertools.proxies.ModuleProxy()

    assert isinstance(module_proxy, scoremanagertools.proxies.ModuleProxy)
