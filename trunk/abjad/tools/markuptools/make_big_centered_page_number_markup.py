from abjad.tools.markuptools.Markup import Markup


def make_big_centered_page_number_markup(text = None):
    r'''.. versionadded:: 1.1

    Make big centered page number markup::

        abjad> markup = markuptools.make_big_centered_page_number_markup()

    ::

        abjad> f(markup)
        \markup {
            \fill-line {
            \bold \fontsize #3 \concat {
            \on-the-fly #print-page-number-check-first
            \fromproperty #'page:page-number-string } } }

    Return markup.

    .. versionchanged:: 2.0
        renamed ``markuptools.big_centered_page_number()`` to
        ``markuptools.make_big_centered_page_number_markup()``.
    '''

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

    markup = Markup(contents)

    return markup
