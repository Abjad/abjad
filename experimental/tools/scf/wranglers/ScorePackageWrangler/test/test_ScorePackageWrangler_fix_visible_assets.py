import scf


def test_ScorePackageWrangler_fix_visible_assets_01():

    studio = scf.studio.Studio()
    wrangler = studio.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_visible_assets(is_interactive=False))
