import os
import scftools

studio = scftools.studio.Studio()
wrangler = studio.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler.breadcrumb == 'materials'


def test_MaterialPackageWrangler_read_only_attributes_02():
    '''Asset containers (all).
    '''

    assert 'materials' in wrangler.list_asset_container_importable_names()
    assert 'example_score_1.mus.materials' in wrangler.list_asset_container_importable_names()
    assert os.environ.get('SCFMATERIALSPATH') in wrangler.list_asset_container_path_names()
    assert os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus', 'materials') in \
        wrangler.list_asset_container_path_names()


def test_MaterialPackageWrangler_read_only_attributes_03():
    '''Current asset container.
    '''

    assert wrangler.current_asset_container_importable_name == 'materials'
    assert wrangler.current_asset_container_path_name == os.environ.get('SCFMATERIALSPATH')


def test_MaterialPackageWrangler_read_only_attributes_04():
    '''Score-external asset container
    '''

    assert wrangler.list_score_external_asset_container_importable_names() == ['materials']
    assert wrangler.list_score_external_asset_container_path_names() == \
        [os.environ.get('SCFMATERIALSPATH')]


def test_MaterialPackageWrangler_read_only_attributes_05():
    '''Score-external assets.
    '''

    assert 'red notes' in wrangler.list_score_external_asset_human_readable_names()
    assert 'materials.red_notes' in wrangler.list_score_external_asset_importable_names()
    assert os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes') in \
        wrangler.list_score_external_asset_path_names()


def test_MaterialPackageWrangler_read_only_attributes_06():
    '''Infix.
    '''

    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.materials'


def test_MaterialPackageWrangler_read_only_attributes_07():
    '''Temporary asset.
    '''

    assert wrangler.temporary_asset_importable_name == 'materials.__temporary_package'
    assert wrangler.temporary_asset_path_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), '__temporary_package')
    assert wrangler.temporary_asset_short_name == '__temporary_package'


def test_MaterialPackageWrangler_read_only_attributes_08():
    '''In-score wrangler.
    '''

    studio = scftools.studio.Studio()
    wrangler = studio.material_package_wrangler
    wrangler.session.current_score_package_short_name = 'example_score_1'
    assert wrangler.session.is_in_score

    assert 'example_score_1.mus.materials' in wrangler.list_asset_container_importable_names()
    assert wrangler.current_asset_container_importable_name == 'example_score_1.mus.materials'
    assert wrangler.temporary_asset_importable_name == 'example_score_1.mus.materials.__temporary_package'
    assert wrangler.temporary_asset_path_name == \
        os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus', 'materials', '__temporary_package')
