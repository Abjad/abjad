import scftools


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    studio = scftools.studio.Studio()
    wrangler = studio.material_package_maker_wrangler

    assert wrangler.breadcrumb == 'material package makers'
    assert wrangler.current_asset_container_importable_name == 'scftools.makers'
    assert all([
        x.startswith('scftools.makers.') for x in wrangler.list_score_external_asset_importable_names()])

    assert wrangler.list_score_external_asset_container_importable_names() == \
        ['scftools.makers']
    assert wrangler.score_internal_asset_container_importable_name_infix is None

    assert wrangler.temporary_asset_importable_name == 'scftools.makers.__temporary_package'

    assert wrangler.list_asset_container_importable_names() == ['scftools.makers']
