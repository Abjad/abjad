from abjad.core.abjadcore import _Abjad


class Markup(_Abjad):

   def __init__(self, contents):
      self.contents = contents
      self.style = 'backslash'

   ## PRIVATE ATTRIBUTES ##

   _styles = ('backslash', 'scheme')

   ## OVERLOADS ##

   def __repr__(self):
      return 'Markup(%s)' % self.contents

   ## PUBLIC ATTRIBUTES ##

   @apply
   def style( ):
      def fget(self):
         return self._style
      def fset(self, arg):
         assert arg in self._styles
         self._style = arg
      return property(**locals( ))
      
   @property
   def format(self):
      if self.style == 'backslash':
         return r'\markup { %s }' % self.contents
      elif self.style == 'scheme':
         return '#%s' % self.contents
      else:
         raise ValueError('unknown markup style.')
