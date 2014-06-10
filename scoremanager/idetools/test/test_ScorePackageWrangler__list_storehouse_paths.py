# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session(is_test=True)


def test_ScorePackageWrangler__list_storehouse_paths_01():
    r'''Lists example score packages directory.
    '''

    wrangler = scoremanager.idetools.ScorePackageWrangler(session=session)
    result = wrangler._list_storehouse_paths(
        abjad_library=False,
        example_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    paths = [
        wrangler._configuration.example_score_packages_directory,
        ]
    assert result == paths