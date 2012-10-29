from abjad import *
import py


def test_markuptools_make_centered_title_markup_01():

    markup = markuptools.make_centered_title_markup('String Quartet')

    assert markup.lilypond_format == '\\markup { \\column { \\center-align { \\override #\'(font-name . "Times") \\fontsize #18 { " " " " " " " " " " \\line { "String Quartet" } " " " " " " } } } }'
    assert markup.indented_lilypond_format == '\\markup {\n\t\\column\n\t\t{\n\t\t\t\\center-align\n\t\t\t\t{\n\t\t\t\t\t\\override\n\t\t\t\t\t\t#\'(font-name . "Times")\n\t\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t\t#18\n\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"String Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t}\n\t\t\t\t}\n\t\t}\n\t}'


def test_markuptools_make_centered_title_markup_02():
    '''List of multiple title lines.
    '''
    py.test.skip('pending scheme pair extension.')

    markup = markuptools.make_centered_title_markup(['String Quartet', 'for the JACK Quartet'])

    assert markup.lilypond_format == '\\markup { \\column { \\center-align { \\override #\'(font-name . Times) \\fontsize #18 { " " " " " " " " " " \\line { "String Quartet" } \\line { "for the JACK Quartet" } " " " " " " } } } }'

    assert markup.indented_lilypond_format == '\\markup {\n\t\\column\n\t\t{\n\t\t\t\\center-align\n\t\t\t\t{\n\t\t\t\t\t\\override\n\t\t\t\t\t\t#\'(font-name . Times)\n\t\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t\t#18\n\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"String Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\\line\n\t\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"for the JACK Quartet"\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t\t" "\n\t\t\t\t\t\t\t}\n\t\t\t\t}\n\t\t}\n\t}'
