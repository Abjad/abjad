# -*- encoding: utf-8 -*-
from experimental import *
from scoremanagertools import specifiers


def test_MusicContributionSpecifierEditor_run_01():

    editor = scoremanagertools.editors.MusicContributionSpecifierEditor()
    editor._run(pending_user_input='id blue~violin~pizzicati add instrument instrument violin done done')

    specifier = specifiers.MusicContributionSpecifier([
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.Violin()
            )
        ],
        custom_identifier='blue violin pizzicati'
        )

    assert editor.target == specifier
