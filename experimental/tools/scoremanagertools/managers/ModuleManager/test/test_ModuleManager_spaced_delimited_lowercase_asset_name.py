# -*- encoding: utf-8 -*-
from experimental import *


def test_ModuleManager_spaced_delimited_lowercase_asset_name_01():

    module_manager = scoremanagertools.managers.ModuleManager()

    assert module_manager._space_delimited_lowercase_name_to_asset_name('foo') == 'foo.py'
    assert module_manager._space_delimited_lowercase_name_to_asset_name('foo bar') == 'foo_bar.py'
