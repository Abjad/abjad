from abjad import *


def test_markuptools_make_centered_title_markup_01():

    markup = markuptools.make_centered_title_markup('String Quartet')

    assert markup.format == '\\markup { \\column {\n            \\center-align {\n                \\override #\'(font-name . "Times")\n                \\fontsize #18 {\n                    " "   " "   " "   " "   " "\n                    \\line { "String Quartet" } \n                    " "   " "   " "\n                }\n            }\n        } }'
