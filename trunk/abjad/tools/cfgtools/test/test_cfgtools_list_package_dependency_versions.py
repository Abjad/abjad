from abjad.tools.cfgtools import *


def test_cfgtools_list_package_dependency_versions_01():

    deps = list_package_dependency_versions()
    assert isinstance(deps, dict)
    assert 'py.test' in deps
    assert isinstance(deps['py.test'], (type(None), str))
    assert 'sphinx' in deps
    assert isinstance(deps['sphinx'], (type(None), str))
