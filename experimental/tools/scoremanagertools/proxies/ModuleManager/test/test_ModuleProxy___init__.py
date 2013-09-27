# -*- encoding: utf-8 -*-
from experimental import *


def test_ModuleManager___init___01():
    r'''Init empty module proxy.
    '''

    module_proxy = scoremanagertools.proxies.ModuleManager()

    assert isinstance(module_proxy, scoremanagertools.proxies.ModuleManager)
