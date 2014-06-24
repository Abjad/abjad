# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetWrangler__list_asset_paths_01():
    r'''Lists paths of example stylesheets.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.StylesheetWrangler(session=session)

    file_names = [
        'clean-letter-14.ily',
        'clean-letter-16.ily',
        'rhythm-letter-16.ily',
        'time-signature-context.ily',
        ]

    paths = []
    for file_name in file_names:
        path = os.path.join(
            wrangler._configuration.example_stylesheets_directory,
            file_name,
            )
        paths.append(path)

    result = wrangler._list_asset_paths(
        abjad_material_packages_and_stylesheets=True,
        example_score_packages=False,
        library=False,
        user_score_packages=False,
        )

    assert result == paths