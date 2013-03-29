from scf.predicates import predicates


def test_predicates_01():

    assert predicates.is_available_underscore_delimited_lowercase_package_name('asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('scf.asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('materials.asdf')

    assert not predicates.is_available_underscore_delimited_lowercase_package_name('scf')
    assert not predicates.is_available_underscore_delimited_lowercase_package_name('materials')


def test_predicates_02():

    assert predicates.is_existing_package_name('scf')
    assert predicates.is_existing_package_name('materials')

    assert not predicates.is_existing_package_name('asdf')
    assert not predicates.is_existing_package_name('scf.asdf')
    assert not predicates.is_existing_package_name('materials.asdf')



def test_predicates_03():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)
