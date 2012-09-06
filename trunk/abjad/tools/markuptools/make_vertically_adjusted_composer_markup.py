def make_vertically_adjusted_composer_markup(composer, 
    font_name='Times', font_size=3, space_above=20, space_right=0):
    r'''.. versionadded:: 2.9

    Make vertically adjusted `composer` markup::

        >>> markup = markuptools.make_vertically_adjusted_composer_markup('Josquin Desprez')

    ::

        >>> print markup.indented_lilypond_format
        \markup {
            \override
                #'(font - name Times)
                {
                    \hspace
                        #0
                    \raise
                        #-20
                        \fontsize
                            #3
                            "Josquin Desprez"
                    \hspace
                        #0
                }
            }

    Return markup.
    '''
    from abjad.tools import markuptools

    assert isinstance(composer, str)
    assert isinstance(font_name, str)
    assert isinstance(font_size, (int, float))
    assert isinstance(space_above, (int, float))
    assert isinstance(space_right, (int, float))

    contents = r'''
        \override #'(font-name . "%s") {
            \hspace #0
            \raise #-%s \fontsize #%s "%s"
            \hspace #%s
        }
       ''' % (font_name, space_above, font_size, composer, space_right)

    return markuptools.Markup(contents)
