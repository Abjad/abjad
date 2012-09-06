def make_big_centered_page_number_markup(text=None):
    r'''.. versionadded:: 1.1

    Make big centered page number markup::

        >>> markup = markuptools.make_big_centered_page_number_markup()

    ::

        >>> print markup.indented_lilypond_format
        \markup {
            \fill-line
                {
                    \bold
                        \fontsize
                            #3
                            \concat
                                {
                                    \on-the-fly
                                        print
                                        page-number-check-first
                                    \fromproperty
                                        page
                                    :page-number-string
                                }
                }
            }

    Return markup.

    .. versionchanged:: 2.0
        renamed ``markuptools.big_centered_page_number()`` to
        ``markuptools.make_big_centered_page_number_markup()``.
    '''
    from abjad.tools import markuptools

    assert isinstance(text, (str, type(None)))

    if text is None:
        contents = r'''
        \fill-line {
        \bold \fontsize #3 \concat {
        \on-the-fly #print-page-number-check-first
        \fromproperty #'page:page-number-string } }'''
    else:
        contents = r'''
        \fill-line {
        \bold \fontsize #3 \concat {
        %s " " \char #x2014 " "
        \on-the-fly #print-page-number-check-first
        \fromproperty #'page:page-number-string } }''' % text

    markup = markuptools.Markup(contents)

    return markup
