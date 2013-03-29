# -*- encoding: utf-8 -*-
import scf


def test_ScorePackageProxy_edit_year_of_completion_interactively_01():

    try:
        studio = scf.studio.Studio()
        studio.run(user_input="L'arch setup year 2001 q")
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == "L'archipel du corps (2011) - setup"
        assert studio.transcript[-2][0] == "L'archipel du corps (2001) - setup"
    finally:
        studio.run(user_input="L'arch setup year 2011 q")
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == "L'archipel du corps (2001) - setup"
        assert studio.transcript[-2][0] == "L'archipel du corps (2011) - setup"
