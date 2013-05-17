from experimental.tools.scoremanagertools.predicates import predicates


def test_predicates_01():

    assert predicates.is_available_underscore_delimited_lowercase_package_name('asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('scoremanagertools.asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('experimental.tools.scoremanagertools.built_in_materials.asdf')

    assert not predicates.is_available_underscore_delimited_lowercase_package_name('scoremanagertools')
    assert not predicates.is_available_underscore_delimited_lowercase_package_name('built_in_materials')


def test_predicates_02():

    assert predicates.is_existing_package_name('scoremanagertools')
    assert predicates.is_existing_package_name('built_in_materials')

    assert not predicates.is_existing_package_name('asdf')
    assert not predicates.is_existing_package_name('scoremanagertools.asdf')
    assert not predicates.is_existing_package_name('experimental.tools.scoremanagertools.built_in_materials.asdf')



def test_predicates_03():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)
