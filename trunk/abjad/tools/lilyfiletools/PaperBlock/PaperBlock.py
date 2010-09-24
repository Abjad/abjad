from abjad.tools.lilyfiletools._BlockAttributed import _BlockAttributed
import types


class PaperBlock(_BlockAttributed):
   r'''.. versionadded:: 1.1.2
   
   Abjad model of LilyPond input file paper block.
   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\paper'
      self.minimal_page_breaking = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _formatted_user_attributes(self):
      result = [ ]
      if self.minimal_page_breaking:
         result.append('#(define page-breaking ly:minimal-breaking)')
      result.extend(_BlockAttributed._formatted_user_attributes.fget(self))
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def minimal_page_breaking( ):
      def fget(self):
         return self._minimal_page_breaking
      def fset(self, expr):
         if isinstance(expr, (bool, type(None))):
            self._minimal_page_breaking = expr
         else:
            raise TypeError('must be boolean or none')
      return property(**locals( ))
