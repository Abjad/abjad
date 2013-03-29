import scf

studio = scf.studio.Studio()
wrangler = studio.material_package_wrangler
assert not wrangler.session.is_in_score


def test_MaterialPackageWrangler_iteration_01():
    '''Assets (all).
    '''

    assert 'red sargasso measures' in wrangler.list_asset_human_readable_names()
    assert 'turquoise pcs' in wrangler.list_asset_human_readable_names()
    assert 'red sargasso measures' not in wrangler.list_asset_human_readable_names(head='aracilik')
    assert 'turquoise pcs' not in wrangler.list_asset_human_readable_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_02():

    assert 'materials.red_sargasso_measures' in \
        wrangler.list_asset_importable_names()
    assert 'manos.mus.materials.turquoise_pcs' in \
        wrangler.list_asset_importable_names()
    assert 'materials.red_sargasso_measures' not in \
        wrangler.list_asset_importable_names(head='aracilik')
    assert 'manos.mus.materials.turquoise_pcs' not in \
        wrangler.list_asset_importable_names(head='aracilik')


def test_MaterialPackageWrangler_iteration_03():

    assert '/Users/trevorbaca/Documents/baca/materials/red_notes' in \
        wrangler.list_asset_path_names()
    assert '/Users/trevorbaca/Documents/baca/materials/red_notes' not in \
        wrangler.list_asset_path_names(head='aracilik')
    assert wrangler.list_asset_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration004():

    # wrangler.list_asset_proxies()
    pass


def test_MaterialPackageWrangler_iteration_05():
    '''Score-internal asset containers.
    '''

    assert 'manos.mus.materials' in \
        wrangler.list_score_internal_asset_container_importable_names()
    assert 'manos.mus.materials' not in \
        wrangler.list_score_internal_asset_container_importable_names(head='aracilik')
    assert wrangler.list_score_internal_asset_container_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_06():

    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials' in \
        wrangler.list_score_internal_asset_container_path_names()
    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials' not in \
        wrangler.list_score_internal_asset_container_path_names(head='aracilik')
    assert wrangler.list_score_internal_asset_container_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_07():
    '''Score-internal assets.
    '''

    assert 'manos.mus.materials.aggregates' in \
        wrangler.list_score_internal_asset_importable_names()
    assert 'manos.mus.materials.aggregates' not in \
        wrangler.list_score_internal_asset_importable_names(head='aracilik')
    assert wrangler.list_score_internal_asset_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_08():

    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials/aggregates' in \
        wrangler.list_score_internal_asset_path_names()
    assert '/Users/trevorbaca/Documents/scores/manos/mus/materials/aggregates' not in \
        wrangler.list_score_internal_asset_path_names(head='aracilik')
    assert wrangler.list_score_internal_asset_path_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_09():
    '''Visible assets.
    '''

    assert 'turquoise pcs' in wrangler.list_visible_asset_human_readable_names()
    assert 'turquoise pcs' not in wrangler.list_visible_asset_human_readable_names(head='aracilik')
    assert wrangler.list_visible_asset_human_readable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_10():

   assert 'manos.mus.materials.turquoise_pcs' in \
        wrangler.list_visible_asset_importable_names()
   assert 'manos.mus.materials.turquoise_pcs' not in \
        wrangler.list_visible_asset_importable_names(head='aracilik')
   assert wrangler.list_visible_asset_importable_names(head='asdf') == []


def test_MaterialPackageWrangler_iteration_11():

    assert ('materials.red_sargasso_measures', 'red sargasso measures') in \
        wrangler.make_visible_asset_menu_tokens()
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') in \
        wrangler.make_visible_asset_menu_tokens()
    assert ('materials.red_sargasso_measures', 'red sargasso measures') not in \
        wrangler.make_visible_asset_menu_tokens(head='aracilik')
    assert ('manos.mus.materials.turquoise_pcs', 'turquoise pcs') not in \
        wrangler.make_visible_asset_menu_tokens(head='aracilik')


def test_MaterialPackageWrangler_iteration_12():

    # wrangler.list_visible_asset_proxies()
    pass
