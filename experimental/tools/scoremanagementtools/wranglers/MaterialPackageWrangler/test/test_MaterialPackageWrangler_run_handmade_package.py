from abjad.tools import notetools
from experimental import *
import py


def test_MaterialPackageWrangler_run_handmade_package_01():
    '''Make handmade package. Delete package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input='m h testnotes default default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_02():
    '''Make handmade package. Corrupt initializer.
    Verify invalid initializer. Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes incanned canned_exception.py default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert not mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
        assert mpp.illustration is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_03():
    '''Make handmade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes incanned canned_exception.py default '
            'inr yes yes default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_04():
    '''Make handmade package. Create output material.
    Delete package."
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py',
            'illustration_builder.py', 'material_definition.py', 'output_material.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_readable_output_material_module
        assert mpp.has_illustration_builder_module
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition and notetools.all_are_notes(mpp.material_definition)
        assert mpp.output_material and notetools.all_are_notes(mpp.output_material)
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_05():
    '''Make handmade package. Delete material definition module.
    Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mddelete remove default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_06():
    '''Make handmade package. Overwrite material definition module with stub.
    Delete package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default '
            'testnotes mdstub default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_07():
    '''Make handmade package. Copy canned material definition. Make output material. Remove output material.
    Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default '
            'omdelete remove default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition and notetools.all_are_notes(mpp.material_definition)
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_08():
    '''Make handmade package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_exception.py default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert not mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_09():
    '''Make handmade package. Copy canned material definition module. Make output data. Corrupt output data.
    Verify invalid output material module. Remove package.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default '
            'omcanned canned_exception.py default q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == ['__init__.py',
            'illustration_builder.py', 'material_definition.py', 'output_material.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert not mpp.has_readable_output_material_module
        assert mpp.has_illustration_builder_module
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition and notetools.all_are_notes(mpp.material_definition)
        assert mpp.output_material is None
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_10():
    '''Make handmade package. Copy canned material definition module.
    Make output data. Make PDF. Remove package.
    '''
    py.test.skip('skip this one during day-to-day development and before build only.')

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testnotes')

    try:
        studio.run(user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default '
            'pdfm default '
            'q')
        assert studio.package_exists('materials.testnotes')
        mpp = scoremanagementtools.proxies.MaterialPackageProxy('materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.directory_contents == [
            '__init__.py', 'illustration.ly', 'illustration.pdf',
            'illustration_builder.py', 'material_definition.py', 'output_material.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_readable_output_material_module
        assert mpp.has_user_finalized_illustration_builder_module
        assert mpp.has_illustration_ly
        assert mpp.has_illustration_pdf
        assert mpp.initializer_has_output_material_safe_import_statement
        assert mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition and notetools.all_are_notes(mpp.material_definition)
        assert mpp.output_material and notetools.all_are_notes(mpp.output_material)
    finally:
        studio.run(user_input='m testnotes del remove default q')
        assert not studio.package_exists('materials.testnotes')
