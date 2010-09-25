from abjad.tools.markuptools.Markup import Markup


def make_big_centered_page_number_markup(text = None):
   r'''.. versionadded:: 1.1.1

   Make big centered page number markup::

      abjad> t = markup.centered_page_number( )
      abjad> print t.format
      \markup { 
         \fill-line {
         \bold \fontsize #3
         \on-the-fly #print-page-number-check-first
         \fromproperty #'page:page-number-string } }

   Return markup.

   .. versionchanged:: 1.1.2
      renamed ``markuptools.big_centered_page_number( )`` to
      ``markuptools.make_big_centered_page_number_markup( )``.
   '''

   assert isinstance(text, (str, type(None)))

   contents = r'''
   \fill-line {
   \bold \fontsize #3 \concat {
   \on-the-fly #print-page-number-check-first
   \fromproperty #'page:page-number-string'''

   if text is None:
      contents += ' } }'
   else:
      #contents += '\n   " - " %s } }' % text
      contents += '\n " "  \char ##x2014 " " %s } }' % text

   markup = Markup(contents)

   return markup
