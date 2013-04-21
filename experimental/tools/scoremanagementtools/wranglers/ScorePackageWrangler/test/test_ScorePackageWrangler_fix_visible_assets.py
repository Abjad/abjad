from experimental import *


def test_ScorePackageWrangler_fix_visible_assets_01():

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    wrangler = score_manager.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_visible_assets(is_interactive=False))
