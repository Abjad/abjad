# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager import specifiers


def test_MusicContributionSpecifierEditor_run_01():

    editor = scoremanager.editors.MusicContributionSpecifierEditor()
    string = 'id blue~violin~pizzicati add instrument instrument violin'
    string += ' done done'
    editor._run(pending_user_input=string)

    specifier = specifiers.MusicContributionSpecifier([
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.Violin()
            )
        ],
        custom_identifier='blue violin pizzicati'
        )

    assert editor.target == specifier
