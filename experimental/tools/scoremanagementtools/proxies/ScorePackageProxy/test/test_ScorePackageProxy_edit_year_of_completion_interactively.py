# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_year_of_completion_interactively_01():

    try:
        studio = scoremanagementtools.studio.Studio()
        studio.run(user_input='example~score setup year 2001 q')
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Example Score I (2013) - setup'
        assert studio.transcript[-2][0] == 'Example Score I (2001) - setup'
    finally:
        studio.run(user_input="example~score setup year 2013 q")
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Example Score I (2001) - setup'
        assert studio.transcript[-2][0] == 'Example Score I (2013) - setup'
