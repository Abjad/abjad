from experimental import *


def test_MaterialPackageWrangler_run_data_only_package_01():
    '''Make data package. Delete package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input='m d testnumbers default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_02():
    '''Make data package. Invalidate initializer.
    Verify invalid initializer. Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers incanned canned_exception.py default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert not mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_03():
    '''Make data package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers incanned canned_exception.py default '
            'inr yes no default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_04():
    '''Make data package. Create output material.
    Delete package."
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == [
            '__init__.py', 'material_definition.py', 'output_material.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_readable_output_material_module
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material == [1, 2, 3, 4, 5]
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_05():
    '''Make data package. Delete material definition module.
    Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mddelete remove default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_06():
    '''Make data package. Overwrite material definition module with stub.
    Delete package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mdstub default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_07():
    '''Make data package. Copy canned material definition. Make output material. Remove output material.
    Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default '
            'omdelete remove default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_08():
    '''Make data package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition_with_exception.py default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert not mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_09():
    '''Make data package. Copy canned material definition module. Make output data. Corrupt output data.
    Verify invalid output material module. Remove package.
    '''

    studio = scftools.studio.Studio()
    assert not studio.package_exists('materials.testnumbers')

    try:
        studio.run(user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default '
            'omcanned canned_exception.py default q')
        assert studio.package_exists('materials.testnumbers')
        mpp = scftools.proxies.MaterialPackageProxy('materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.directory_contents == [
            '__init__.py', 'material_definition.py', 'output_material.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert not mpp.has_readable_output_material_module
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnumbers del remove default q')
        assert not studio.package_exists('materials.testnumbers')
