# -*- encoding: utf-8 -*-
import pytest
from experimental import *
pytest.skip('skipping temporarily.')


def test_ScorePackageWrangler_fix_visible_assets_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.score_package_wrangler
    wrangler.session.display_all_scores()

    assert all(wrangler.fix_visible_assets(is_interactive=False))
