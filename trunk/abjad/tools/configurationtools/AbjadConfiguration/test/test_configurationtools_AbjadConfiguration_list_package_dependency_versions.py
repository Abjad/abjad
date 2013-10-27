# -*- encoding: utf-8 -*-
from abjad import *


def test_configurationtools_AbjadConfiguration_list_package_dependency_versions_01():

    deps = configurationtools.AbjadConfiguration.list_package_dependency_versions()
    assert isinstance(deps, dict)
    assert 'py.test' in deps
    assert isinstance(deps['py.test'], (type(None), str))
    assert 'sphinx' in deps
    assert isinstance(deps['sphinx'], (type(None), str))
