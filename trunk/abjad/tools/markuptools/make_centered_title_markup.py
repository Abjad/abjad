def make_centered_title_markup(title, font_name='Times', font_size=18):
    r'''.. versionadded:: 2.9
    
    Make centered `title` markup::

        >>> markup = markuptools.make_centered_title_markup('String Quartet')

    ::

        >>> print markup.indented_lilypond_format
        \markup {
            \column
                {
                    \center-align
                        {
                            \override
                                #'(font - name Times)
                                \fontsize
                                    #18
                                    {
                                        " "
                                        " "
                                        " "
                                        " "
                                        " "
                                        \line
                                            {
                                                "String Quartet"
                                            }
                                        " "
                                        " "
                                        " "
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

    contents = r'''\column {
            \center-align {
                \override #'(font-name . "%s")
                \fontsize #%s {
                    " "   " "   " "   " "   " "
                    \line { "%s" } 
                    " "   " "   " "
                }
            }
        }''' % (font_name, font_size, title)

    return markuptools.Markup(contents)
