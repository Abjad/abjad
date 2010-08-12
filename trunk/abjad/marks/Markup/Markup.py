from abjad.core import _Abjad
from abjad.core import _Immutable
import types


class Markup(_Abjad, _Immutable):
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

   def __init__(self, arg, style = 'backslash'):
      if isinstance(arg, str):
         #self._contents = arg
         #self.style = 'backslash'
         contents = arg
         style = style
      elif isinstance(self, Markup):
         #self._contents = arg.contents
         #self.style = arg.style
         contents = arg.contents
         style = arg.style
      else:
         raise TypeError('must be string or other markup instance.')
      object.__setattr__(self, 'contents', contents)
      object.__setattr__(self, 'style', style)
      
   ## PRIVATE ATTRIBUTES ##

   _styles = ('backslash', 'scheme')

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, Markup):
         if self.format == arg.format:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.contents)

   def __str__(self):
      return self.format

   ## PUBLIC ATTRIBUTES ##

#   @property
#   def contents(self):
#      '''Read-only content string.'''
#      return self._contents

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

#   @apply
#   def style( ):
#      def fget(self):
#         '''Read / write attribute set to either 
#         ``'backslash'`` or ``'scheme'``.
#
#         Default to 'backslash'. ::
#
#            abjad> markup = Markup('"This is markup text."')
#            abjad> markup.style
#            'backslash'
#         '''
#         return self._style
#      def fset(self, arg):
#         assert arg in self._styles
#         self._style = arg
#      return property(**locals( ))
