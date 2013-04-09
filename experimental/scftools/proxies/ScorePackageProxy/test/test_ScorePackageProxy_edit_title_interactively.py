# -*- encoding: utf-8 -*-
import scftools


def test_ScorePackageProxy_edit_title_interactively_01():

    try:
        studio = scftools.studio.Studio()
        studio.run(user_input='betorung setup title Foo q')
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Betörung (2012) - setup'
        assert studio.transcript[-2][0] == 'Foo (2012) - setup'
    finally:
        studio.run(user_input='foo setup title Betörung q')
        assert studio.ts == (9,)
        assert studio.transcript[-5][0] == 'Foo (2012) - setup'
        assert studio.transcript[-2][0] == 'Betörung (2012) - setup'
