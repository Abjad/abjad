# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()


def test_MaterialPackageWrangler__get_available_path_01():

    session = scoremanager.idetools.Session(is_test=True)
    session._set_test_score('red_example_score')
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)
    input_ = 'foo'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    path = os.path.join(
        configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'foo',
        )

    assert result == path


def test_MaterialPackageWrangler__get_available_path_02():

    session = scoremanager.idetools.Session(is_test=True)
    wrangler = scoremanager.idetools.MaterialPackageWrangler(session=session)

    input_ = 'q'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None

    input_ = 'b'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None

    input_ = 'ss'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None