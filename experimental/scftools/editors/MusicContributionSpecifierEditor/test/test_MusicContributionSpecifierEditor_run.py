import scftools
from abjad import *
from scftools import specifiers


def test_MusicContributionSpecifierEditor_run_01():

    editor = scftools.editors.MusicContributionSpecifierEditor()
    editor.run(user_input='name blue~violin~pizzicati add instrument instrument violin done done')

    specifier = specifiers.MusicContributionSpecifier([
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.Violin()
            )
        ],
        name='blue violin pizzicati'
        )

    assert editor.target == specifier
