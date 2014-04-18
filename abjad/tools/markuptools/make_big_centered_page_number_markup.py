# -*- encoding: utf-8 -*-


def make_big_centered_page_number_markup(text=None):
    r'''Make big centered page number markup:

    ::

        >>> markup = markuptools.make_big_centered_page_number_markup()

    ::

        >>> print(format(markup, 'lilypond'))
        \markup {
            \fill-line
                {
                    \bold
                        \fontsize
                            #3
                            \concat
                                {
                                    \on-the-fly
                                        #print-page-number-check-first
                                        \fromproperty
                                            #'page:page-number-string
                                }
                }
            }

    Returns markup.
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
