def make_centered_title_markup(title, font_name='Times', font_size=18, vspace_before=6, vspace_after=12):
    r'''.. versionadded:: 2.9
    
    Make centered `title` markup::

        >>> markup = markuptools.make_centered_title_markup('String Quartet')

    ::

        >>> print markup.indented_lilypond_format
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

    Return markup.
    '''
    from abjad.tools import markuptools

    assert isinstance(title, str)
    assert isinstance(font_name, str)
    assert isinstance(font_size, (int, float))

    contents = r'''
        \override #'(font-name . "%s")
        \fontsize #%s 
        \column {
            \center-align {
                {
                    \vspace #%s
                    \line { "%s" } 
                    \vspace #%s
                }
            }
        }''' % (font_name, font_size, vspace_before, title, vspace_after)

    return markuptools.Markup(contents)
