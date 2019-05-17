import abjad


def test_AbjadConfiguration_list_package_dependency_versions_01():

    deps = abjad.AbjadConfiguration.list_package_dependency_versions()
    assert isinstance(deps, dict)
    assert "pytest" in deps
    assert isinstance(deps["pytest"], (type(None), str))
    assert "sphinx" in deps
    assert isinstance(deps["sphinx"], (type(None), str))
