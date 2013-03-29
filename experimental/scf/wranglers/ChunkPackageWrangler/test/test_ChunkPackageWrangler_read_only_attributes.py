import scf


def test_ChunkPackageWrangler_read_only_attributes_01():

    studio = scf.studio.Studio()
    wrangler = studio.chunk_package_wrangler
    assert not wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'sketches'
    assert wrangler.current_asset_container_importable_name == 'sketches'
    assert all([x.startswith('sketches') for x in wrangler.list_score_external_asset_importable_names()])

    assert wrangler.list_score_external_asset_container_importable_names() == ['sketches']
    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.chunks'

    assert wrangler.temporary_asset_importable_name == 'sketches.__temporary_package'

    assert 'sketches' in wrangler.list_asset_container_importable_names()
    assert 'aracilik.mus.chunks' in wrangler.list_asset_container_importable_names()


def test_ChunkPackageWrangler_read_only_attributes_02():

    studio = scf.studio.Studio()
    wrangler = studio.chunk_package_wrangler
    wrangler.session.current_score_package_short_name = 'aracilik'
    assert wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'chunks'

    assert wrangler.current_asset_container_importable_name == 'aracilik.mus.chunks'

    assert all([
        x.startswith('sketches.') for x in wrangler.list_score_external_asset_importable_names()])
    assert wrangler.list_score_external_asset_container_importable_names() == \
        ['sketches']

    assert wrangler.score_internal_asset_container_importable_name_infix == 'mus.chunks'

    assert wrangler.temporary_asset_importable_name == 'aracilik.mus.chunks.__temporary_package'

    assert 'sketches' in wrangler.list_asset_container_importable_names()
    assert 'aracilik.mus.chunks' in wrangler.list_asset_container_importable_names()
