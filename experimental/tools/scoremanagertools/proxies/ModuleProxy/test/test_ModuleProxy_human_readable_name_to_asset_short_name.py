from experimental import *


def test_ModuleProxy_human_readable_name_to_asset_name_01():

    module_proxy = scoremanagertools.proxies.ModuleProxy()

    assert module_proxy.human_readable_name_to_asset_name('foo') == 'foo.py'
    assert module_proxy.human_readable_name_to_asset_name('foo bar') == 'foo_bar.py'
