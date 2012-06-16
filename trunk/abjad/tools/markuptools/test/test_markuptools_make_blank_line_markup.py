from abjad import *


def test_markuptools_make_blank_line_markup_01():

    markup = markuptools.make_blank_line_markup()

    assert markup.lilypond_format == '\\markup { \\fill-line { " " } }'
