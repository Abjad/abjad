# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_make_centered_title_markup_01():

    markup = markuptools.make_centered_title_markup('String Quartet')

    assert systemtools.TestManager.compare(
        format(markup, 'lilypond'),
        r'''
        \markup {
            \override
                #'(font-name . "Times")
                \fontsize
                    #18
                    \column
                        {
                            \center-align
                                {
                                    {
                                        \vspace
                                            #6
                                        \line
                                            {
                                                "String Quartet"
                                            }
                                        \vspace
                                            #12
                                    }
                                }
                        }
            }
        ''',
        )


def test_markuptools_make_centered_title_markup_02():
    r'''List of multiple title lines.
    '''

    markup = markuptools.make_centered_title_markup(
        ['String Quartet', 'for the JACK Quartet'],
        )

    assert systemtools.TestManager.compare(
        format(markup, 'lilypond'),
        r'''
        \markup {
            \override
                #'(font-name . "Times")
                \fontsize
                    #18
                    \column
                        {
                            \center-align
                                {
                                    {
                                        \vspace
                                            #6
                                        \line
                                            {
                                                "String Quartet"
                                            }
                                        \line
                                            {
                                                "for the JACK Quartet"
                                            }
                                        \vspace
                                            #12
                                    }
                                }
                        }
            }
        ''',
        )
