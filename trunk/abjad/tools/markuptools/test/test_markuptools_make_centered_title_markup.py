from abjad import *


def test_markuptools_make_centered_title_markup_01():

    markup = markuptools.make_centered_title_markup('String Quartet')

    assert markup.lilypond_format == '\\markup { \\override #\'(font-name . "Times") \\fontsize #18 \\column { \\center-align { { \\vspace #6 \\line { "String Quartet" } \\vspace #12 } } } }'

    assert markup.indented_lilypond_format == '\\markup {\n\t\\override\n\t\t#\'(font-name . "Times")\n\t\t\\fontsize\n\t\t\t#18\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\center-align\n\t\t\t\t\t\t{\n\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\\vspace\n\t\t\t\t\t\t\t\t\t#6\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"String Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\\vspace\n\t\t\t\t\t\t\t\t\t#12\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}\n\t\t\t\t}\n\t}'


def test_markuptools_make_centered_title_markup_02():
    '''List of multiple title lines.
    '''

    markup = markuptools.make_centered_title_markup(['String Quartet', 'for the JACK Quartet'])

    assert markup.lilypond_format == '\\markup { \\override #\'(font-name . "Times") \\fontsize #18 \\column { \\center-align { { \\vspace #6 \\line { "String Quartet" } \\line { "for the JACK Quartet" } \\vspace #12 } } } }'

    assert markup.indented_lilypond_format == '\\markup {\n\t\\override\n\t\t#\'(font-name . "Times")\n\t\t\\fontsize\n\t\t\t#18\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\center-align\n\t\t\t\t\t\t{\n\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\\vspace\n\t\t\t\t\t\t\t\t\t#6\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"String Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"for the JACK Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\\vspace\n\t\t\t\t\t\t\t\t\t#12\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}\n\t\t\t\t}\n\t}'
