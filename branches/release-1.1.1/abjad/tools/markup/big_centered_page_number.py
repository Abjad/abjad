from abjad.markup import Markup
import types


def big_centered_page_number(text = None):
   r'''.. versionadded:: 1.1.1

   Return Abjad centered page number :class:`~abjad.Markup`.

   ::

      abjad> t = markup.centered_page_number( )
      abjad> print t.format
      \markup { 
         \fill-line {
         \bold \fontsize #3
         \on-the-fly #print-page-number-check-first
         \fromproperty #'page:page-number-string } }
   '''

   assert isinstance(text, (str, types.NoneType))

   markup = Markup( )
   markup.contents = r'''
   \fill-line {
   \bold \fontsize #3 \concat {
   \on-the-fly #print-page-number-check-first
   \fromproperty #'page:page-number-string'''

   if text is None:
      markup.contents += ' } }'
   else:
      markup.contents += '\n   " - " %s } }' % text

   return markup
