import scf


def test_MaterialPackageWrangler_make_numeric_sequence_package_01():

    wrangler = scf.wranglers.MaterialPackageWrangler()
    assert not wrangler.package_exists('materials.testsequence')

    try:
        wrangler.make_numeric_sequence_package('materials.testsequence')
        assert wrangler.package_exists('materials.testsequence')
        mpp = scf.proxies.MaterialPackageProxy('materials.testsequence')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.package_exists('materials.testsequence')


def test_MaterialPackageWrangler_make_numeric_sequence_package_02():
    '''Interactively.
    '''

    wrangler = scf.wranglers.MaterialPackageWrangler()
    assert not wrangler.package_exists('materials.testsequence')

    try:
        wrangler.make_numeric_sequence_package_interactively(user_input='testsequence')
        assert wrangler.package_exists('materials.testsequence')
        mpp = scf.proxies.MaterialPackageProxy('materials.testsequence')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.package_exists('materials.testsequence')
