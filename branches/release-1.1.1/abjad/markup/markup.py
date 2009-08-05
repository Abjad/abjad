from abjad.core.abjadcore import _Abjad
import types


class Markup(_Abjad):
   r'''Abjad wrapper around LilyPond markup.

   Class inserts ``\markup { }`` wrapper around contents at format time. ::

      abjad> markup = Markup(r'\bold { "This is markup text." }')
      abjad> print markup.format
      \markup { \bold { "This is markup text." } }

   ::

      abjad> markup.contents = '"New markup contents."'
      abjad> print markup.format
      \markup { "New markup contents." }

   Markup contents must be set by hand.
   '''

   def __init__(self, contents = None):
      self.contents = contents
      self.style = 'backslash'

   ## PRIVATE ATTRIBUTES ##

   _styles = ('backslash', 'scheme')

   ## OVERLOADS ##

   def __repr__(self):
      return 'Markup(%s)' % self.contents

   ## PUBLIC ATTRIBUTES ##

   @apply
   def contents( ):
      def fget(self):
         '''Read / write string equal to markup contents.
         
         ::
   
            abjad> markup = Markup('"This is markup text."')
            abjad> markup.contents
            '"This is markup text."'
         '''
         return self._contents
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         if isinstance(arg, str):
            self._contents = arg
         elif isinstance(arg, types.NoneType):
            self._contents = ''
      return property(**locals( ))

   @property
   def format(self):
      '''Read-only LilyPond string of `self`.

      ::

         abjad> markup = Markup('"This is markup text.'")
         abjad> print markup.format
         \markup { "This is markup text." }
      '''
      if self.style == 'backslash':
         return r'\markup { %s }' % self.contents
      elif self.style == 'scheme':
         return '#%s' % self.contents
      else:
         raise ValueError('unknown markup style.')

   @apply
   def style( ):
      def fget(self):
         '''Read / write attribute set to either 
         ``'backslash'`` or ``'scheme'``.

         Default to 'backslash'. ::

            abjad> markup = Markup('"This is markup text."')
            abjad> markup.style
            'backslash'
         '''
         return self._style
      def fset(self, arg):
         assert arg in self._styles
         self._style = arg
      return property(**locals( ))
